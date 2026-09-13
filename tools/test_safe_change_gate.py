#!/usr/bin/env python3
"""Tests for the recovery declarations the SAFE-CHANGE gate must enforce."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
TOOLS = REPO / "tools"

BASE_FILL = {
    "target: UNKNOWN": "target: probe",
    "recovery_actor: UNKNOWN": "recovery_actor: human-operator",
    "where_to_act: UNKNOWN": "where_to_act: probe-workspace",
    "changed: UNKNOWN": "changed: config-file",
    "known_good: UNKNOWN": "known_good: git-base-commit",
    "restart_or_new_session: UNKNOWN": "restart_or_new_session: new-session",
    "verify_operation: UNKNOWN": "verify_operation: probe-check",
    "verify_communication: UNKNOWN": "verify_communication: NOT_NEEDED",
    "restore_only: UNKNOWN": "restore_only: config-file",
    "fallback: UNKNOWN": "fallback: NOT_NEEDED",
    "touches_only_communication_path: UNKNOWN": "touches_only_communication_path: false",
    "touches_only_recovery_path: UNKNOWN": "touches_only_recovery_path: false",
}
HOST_TIMER = "systemd-timer ena-rollback.timer"


class SafeChangeGateTests(unittest.TestCase):
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
        return subprocess.run(
            [sys.executable, *map(str, args)],
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
        )

    def rescue_text(self) -> str:
        return (self.package / "rescue.yaml").read_text(encoding="utf-8")

    def replace_rescue(self, old: str, new: str) -> None:
        path = self.package / "rescue.yaml"
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text)
        path.write_text(text.replace(old, new), encoding="utf-8")

    def fill_rescue(
        self,
        *,
        rollback_action: str = "git-revert-change",
        automatic_rollback: str = "false",
        automatic_rollback_reference: str = "null",
    ) -> None:
        text = self.rescue_text()
        for old, new in BASE_FILL.items():
            text = text.replace(old, new)
        text = text.replace("rollback_action: UNKNOWN", f"rollback_action: {rollback_action}")
        text = text.replace("automatic_rollback: null", f"automatic_rollback: {automatic_rollback}")
        text = text.replace(
            "automatic_rollback_reference: null",
            f"automatic_rollback_reference: {automatic_rollback_reference}",
        )
        (self.package / "rescue.yaml").write_text(text, encoding="utf-8")

    def configure_script(self) -> None:
        (self.package / "rollback.py").write_text(
            "#!/usr/bin/env python3\nprint('restore previous working state')\n",
            encoding="utf-8",
        )

    def arm(self):
        return self.run_tool(TOOLS / "safe_change_state.py", self.package, "armed")

    def transition(self) -> dict:
        lines = [
            json.loads(line)
            for line in (self.package / "transitions.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        return lines[-1]

    def reset_to_preparing(self) -> None:
        (self.package / "transitions.jsonl").unlink(missing_ok=True)
        status = self.package / "status.yaml"
        status.write_text(
            status.read_text(encoding="utf-8").replace("state: armed", "state: preparing"),
            encoding="utf-8",
        )

    def test_scaffold_uses_rescue_schema_04_and_explicit_unknowns(self):
        text = self.rescue_text()
        self.assertIn("schema_version: '0.4'", text)
        for key in (
            "verify_communication",
            "restore_only",
            "fallback",
            "touches_only_communication_path",
            "touches_only_recovery_path",
        ):
            self.assertIn(f"{key}: UNKNOWN", text)

    def test_unresolved_rescue_declarations_block_armed(self):
        self.fill_rescue()
        for key, resolved in (
            ("verify_communication", "NOT_NEEDED"),
            ("restore_only", "config-file"),
            ("fallback", "NOT_NEEDED"),
        ):
            with self.subTest(key=key):
                self.replace_rescue(f"{key}: {resolved}", f"{key}: UNKNOWN")
                result = self.arm()
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertIn(f"rescue.yaml {key}", result.stderr)
                self.replace_rescue(f"{key}: UNKNOWN", f"{key}: {resolved}")

    def test_not_needed_is_exact_for_communication_and_fallback(self):
        self.fill_rescue()
        self.assertEqual(self.arm().returncode, 0)
        self.reset_to_preparing()

        self.replace_rescue("verify_communication: NOT_NEEDED", "verify_communication: not_needed")
        result = self.arm()
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("exact NOT_NEEDED", result.stderr)
        self.replace_rescue("verify_communication: not_needed", "verify_communication: NOT_NEEDED")

        self.replace_rescue("fallback: NOT_NEEDED", "fallback: NOT_APPLICABLE")
        result = self.arm()
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("exact NOT_NEEDED", result.stderr)

    def test_restore_scope_requires_concrete_declaration(self):
        self.fill_rescue()
        self.replace_rescue("restore_only: config-file", "restore_only: NOT_NEEDED")
        result = self.arm()
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("restore_only must be a concrete declaration", result.stderr)

    def test_single_path_flags_require_exact_booleans(self):
        self.fill_rescue()
        for value in ("TRUE", "yes", "UNKNOWN"):
            with self.subTest(value=value):
                self.replace_rescue(
                    "touches_only_communication_path: false",
                    f"touches_only_communication_path: {value}",
                )
                result = self.arm()
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertIn("must be exactly true or false", result.stderr)
                self.replace_rescue(
                    f"touches_only_communication_path: {value}",
                    "touches_only_communication_path: false",
                )

    def test_both_single_paths_true_block_armed(self):
        self.fill_rescue()
        self.replace_rescue("touches_only_communication_path: false", "touches_only_communication_path: true")
        self.replace_rescue("touches_only_recovery_path: false", "touches_only_recovery_path: true")
        result = self.arm()
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("touches both the only communication path", result.stderr)

    def test_other_single_path_boolean_combinations_can_arm(self):
        for communication, recovery in (("false", "false"), ("true", "false"), ("false", "true")):
            with self.subTest(communication=communication, recovery=recovery):
                self.fill_rescue()
                self.replace_rescue(
                    "touches_only_communication_path: false",
                    f"touches_only_communication_path: {communication}",
                )
                self.replace_rescue(
                    "touches_only_recovery_path: false",
                    f"touches_only_recovery_path: {recovery}",
                )
                result = self.arm()
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.reset_to_preparing()

    def test_armed_transition_records_declared_rescue_basis(self):
        self.fill_rescue()
        result = self.arm()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        transition = self.transition()
        self.assertEqual(transition["verify_communication"], "NOT_NEEDED")
        self.assertEqual(transition["restore_only"], "config-file")
        self.assertEqual(transition["fallback"], "NOT_NEEDED")
        self.assertIs(transition["touches_only_communication_path"], False)
        self.assertIs(transition["touches_only_recovery_path"], False)

        before = (self.package / "transitions.jsonl").read_bytes()
        self.replace_rescue("restore_only: config-file", "restore_only: later-edit")
        self.assertEqual((self.package / "transitions.jsonl").read_bytes(), before)

    def test_old_rescue_schema_requires_reconciliation(self):
        self.fill_rescue()
        self.replace_rescue("schema_version: '0.4'", "schema_version: '0.3'")
        result = self.arm()
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("schema_version must be 0.4", result.stderr)
        self.assertIn("reconcile older SAFE-CHANGE packages", result.stderr)

    def test_automatic_rollback_typo_blocks(self):
        for value in ("flase", "maybe", "yes", "1"):
            with self.subTest(value=value):
                self.fill_rescue(automatic_rollback=value)
                result = self.arm()
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertIn("is not a declaration", result.stderr)

    def test_automatic_true_requires_reference(self):
        self.fill_rescue(automatic_rollback="true")
        result = self.arm()
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("automatic_rollback_reference is unresolved", result.stderr)

    def test_automatic_true_with_reference_arms_without_local_script(self):
        self.fill_rescue(
            automatic_rollback="true",
            automatic_rollback_reference=HOST_TIMER,
        )
        (self.package / "rollback.py").unlink()
        result = self.arm()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        transition = self.transition()
        self.assertEqual(transition["rollback_mode"], "declared_automatic")
        self.assertEqual(transition["rollback_artifact"], "absent")
        self.assertEqual(transition["automatic_rollback_reference"], HOST_TIMER)

    def test_false_with_automatic_reference_is_contradictory(self):
        self.fill_rescue(
            automatic_rollback="false",
            automatic_rollback_reference=HOST_TIMER,
        )
        result = self.arm()
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("automatic_rollback is false", result.stderr)

    def test_manual_declaration_arms_with_placeholder_artifact(self):
        self.fill_rescue(automatic_rollback="false")
        result = self.arm()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        transition = self.transition()
        self.assertEqual(transition["rollback_mode"], "declared_manual_or_host_triggered")
        self.assertEqual(transition["rollback_artifact"], "placeholder")

    def test_undeclared_placeholder_cannot_arm(self):
        self.fill_rescue(automatic_rollback="null")
        result = self.arm()
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("automatic_rollback: false", result.stderr)

    def test_configured_script_can_arm_without_automaticity_declaration(self):
        self.configure_script()
        self.fill_rescue(automatic_rollback="null")
        result = self.arm()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        transition = self.transition()
        self.assertEqual(transition["rollback_mode"], "not_declared")
        self.assertEqual(transition["rollback_artifact"], "configured_script")
        self.assertNotIn("automatic_rollback_reference", transition)

    def test_placeholder_script_cannot_satisfy_rollback_action_claim(self):
        self.fill_rescue(
            rollback_action="python rollback.py",
            automatic_rollback="false",
        )
        result = self.arm()
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("points at rollback.py", result.stderr)

    def test_terminal_states_still_require_evidence(self):
        self.fill_rescue()
        for state in ("armed", "applied"):
            result = self.run_tool(TOOLS / "safe_change_state.py", self.package, state)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        no_evidence = self.run_tool(TOOLS / "safe_change_state.py", self.package, "retained")
        self.assertEqual(no_evidence.returncode, 2, no_evidence.stdout + no_evidence.stderr)
        self.assertIn("requires --evidence", no_evidence.stderr)

    def test_full_lifecycle_keeps_armed_basis_in_history(self):
        self.fill_rescue()
        for state in ("armed", "applied"):
            result = self.run_tool(TOOLS / "safe_change_state.py", self.package, state)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        retained = self.run_tool(
            TOOLS / "safe_change_state.py",
            self.package,
            "retained",
            "--evidence",
            "probe-validation",
        )
        self.assertEqual(retained.returncode, 0, retained.stdout + retained.stderr)
        lines = [
            json.loads(line)
            for line in (self.package / "transitions.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(lines[0]["restore_only"], "config-file")
        self.assertNotIn("restore_only", lines[-1])
        self.assertIn("state: retained", (self.package / "status.yaml").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
