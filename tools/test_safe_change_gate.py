#!/usr/bin/env python3
"""Tests for the recovery declaration the SAFE-CHANGE gate must enforce."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
TOOLS = REPO / "tools"

RESCUE_FILL = {
    "target: UNKNOWN": "target: probe",
    "recovery_actor: UNKNOWN": "recovery_actor: human-operator",
    "where_to_act: UNKNOWN": "where_to_act: probe-workspace",
    "changed: UNKNOWN": "changed: config-file",
    "known_good: UNKNOWN": "known_good: git-base-commit",
    "restart_or_new_session: UNKNOWN": "restart_or_new_session: new-session",
    "verify_operation: UNKNOWN": "verify_operation: probe-check",
}


class RollbackDeclarationTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.home = self.tmp / "home"
        result = self.run_tool(
            TOOLS / "ena_init.py",
            "--home", self.home,
            "--timezone", "Etc/UTC",
            "--language", "en-US",
            "--host-profile", "session",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

        scaffold = self.run_tool(
            TOOLS / "change_scaffold.py",
            "--home", self.home,
            "--name", "probe",
            "--profile", "session",
        )
        self.assertEqual(scaffold.returncode, 0, scaffold.stdout + scaffold.stderr)
        self.package = Path(scaffold.stdout.strip())

    def tearDown(self):
        self._tmp.cleanup()

    def run_tool(self, *args):
        return subprocess.run([sys.executable, *map(str, args)], text=True, capture_output=True)

    def write_rescue(self, *, rollback_action: str, automatic_rollback: str) -> None:
        text = (self.package / "rescue.yaml").read_text(encoding="utf-8")
        for old, new in RESCUE_FILL.items():
            text = text.replace(old, new)
        text = text.replace("rollback_action: UNKNOWN", f"rollback_action: {rollback_action}")
        text = text.replace("automatic_rollback: null", f"automatic_rollback: {automatic_rollback}")
        (self.package / "rescue.yaml").write_text(text, encoding="utf-8")

    def arm(self):
        return self.run_tool(TOOLS / "safe_change_state.py", self.package, "armed")

    def transition(self) -> dict:
        lines = [
            json.loads(line)
            for line in (self.package / "transitions.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        return lines[-1]

    # ------------------------------------------------------------------ cases

    def test_undeclared_placeholder_cannot_arm(self):
        self.write_rescue(rollback_action="git-revert-change", automatic_rollback="null")
        result = self.arm()
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("automatic_rollback: false", result.stderr)
        self.assertFalse((self.package / "transitions.jsonl").exists())

    def test_declared_manual_rollback_arms_and_is_recorded(self):
        self.write_rescue(rollback_action="git-revert-change", automatic_rollback="false")
        result = self.arm()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.transition()["rollback_mode"], "declared_no_automatic_rollback")

    def test_claiming_automatic_rollback_with_a_placeholder_is_blocked(self):
        self.write_rescue(rollback_action="git-revert-change", automatic_rollback="true")
        result = self.arm()
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("automatic_rollback is true", result.stderr)

    def test_rollback_action_pointing_at_the_placeholder_is_blocked(self):
        self.write_rescue(rollback_action="python rollback.py", automatic_rollback="false")
        result = self.arm()
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("points at rollback.py", result.stderr)

    def test_configured_rollback_script_needs_no_declaration(self):
        (self.package / "rollback.py").write_text(
            "#!/usr/bin/env python3\nprint('restore the previous working state')\n", encoding="utf-8"
        )
        self.write_rescue(rollback_action="python rollback.py", automatic_rollback="null")
        result = self.arm()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.transition()["rollback_mode"], "executable_script")

    def test_missing_rollback_script_also_needs_the_declaration(self):
        (self.package / "rollback.py").unlink()
        self.write_rescue(rollback_action="git-revert-change", automatic_rollback="null")
        blocked = self.arm()
        self.assertEqual(blocked.returncode, 2, blocked.stdout + blocked.stderr)
        self.assertIn("no rollback.py", blocked.stderr)

        self.write_rescue(rollback_action="git-revert-change", automatic_rollback="false")
        armed = self.arm()
        self.assertEqual(armed.returncode, 0, armed.stdout + armed.stderr)
        self.assertEqual(self.transition()["rollback_mode"], "declared_no_automatic_rollback")

    def test_unresolved_recovery_facts_still_block_arming(self):
        (self.package / "rescue.yaml").write_text(
            "schema_version: '0.3'\nhost_profile: session\nautomatic_rollback: false\n", encoding="utf-8"
        )
        result = self.arm()
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("rollback_action is unresolved", result.stderr)

    def test_full_lifecycle_keeps_the_declaration_in_history(self):
        self.write_rescue(rollback_action="git-revert-change", automatic_rollback="false")
        for state in ("armed", "applied"):
            result = self.run_tool(TOOLS / "safe_change_state.py", self.package, state)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        retained = self.run_tool(
            TOOLS / "safe_change_state.py", self.package, "retained", "--evidence", "probe-validation"
        )
        self.assertEqual(retained.returncode, 0, retained.stdout + retained.stderr)
        self.assertIsNone(self.transition().get("rollback_mode"))
        self.assertIn("state: retained", (self.package / "status.yaml").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
