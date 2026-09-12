#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from control_yaml import parse_control_yaml


REPO = Path(__file__).resolve().parents[1]
TOOLS = REPO / "tools"


class UpgradeMigrationTests(unittest.TestCase):
    def run_tool(self, name: str, *args: object):
        return subprocess.run(
            [sys.executable, str(TOOLS / name), *map(str, args)],
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
        )

    def test_pre_provenance_ready_home_gets_migration_diagnostic_and_can_recover(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            home = Path(tmpdir) / "home"
            created = self.run_tool(
                "ena_init.py",
                "--home", home,
                "--timezone", "Etc/UTC",
                "--language", "en-US",
                "--recovery", "git-revert",
                "--rescuer", "operator-console",
                "--rescuer-type", "human",
            )
            self.assertEqual(created.returncode, 0, created.stdout + created.stderr)

            system_path = home / "SYSTEM.yaml"
            text = system_path.read_text(encoding="utf-8").replace(
                "minimum_ready: false", "minimum_ready: true", 1
            )
            system_path.write_text(text, encoding="utf-8")
            before = system_path.read_bytes()

            preflight = self.run_tool("ena_preflight.py", "--home", home)
            self.assertEqual(preflight.returncode, 2, preflight.stdout + preflight.stderr)
            self.assertIn("pre-provenance READY home", preflight.stdout)
            self.assertIn("re-verify and re-assert", preflight.stdout)
            self.assertNotIn("recovery.verification_confidence must be SELF_ASSERTED", preflight.stdout)
            self.assertEqual(system_path.read_bytes(), before)

            inspected = self.run_tool("ena_first_use.py", "--home", home)
            self.assertEqual(inspected.returncode, 2, inspected.stdout + inspected.stderr)
            self.assertIn("pre-provenance READY home", inspected.stdout)
            self.assertEqual(system_path.read_bytes(), before)

            migrated = self.run_tool(
                "ena_first_use.py",
                "--home", home,
                "--verified-recovery", "git-revert",
                "--recovery-evidence", "restore-drill:current",
                "--verified-rescuer", "operator-console",
                "--rescuer-evidence", "reachability-check:current",
                "--rescuer-type", "human",
            )
            self.assertEqual(migrated.returncode, 0, migrated.stdout + migrated.stderr)
            self.assertIn("ENA First Use: READY", migrated.stdout)

            current = parse_control_yaml(system_path.read_text(encoding="utf-8"))
            self.assertEqual(current["recovery"]["verification_confidence"], "SELF_ASSERTED")
            self.assertEqual(current["rescue"]["verification_confidence"], "SELF_ASSERTED")
            self.assertIn("verified_at", current["recovery"])
            self.assertIn("verified_at", current["rescue"])

            final_preflight = self.run_tool("ena_preflight.py", "--home", home)
            self.assertEqual(final_preflight.returncode, 0, final_preflight.stdout + final_preflight.stderr)

    def test_partial_provenance_is_not_mislabeled_as_legacy(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            home = Path(tmpdir) / "home"
            created = self.run_tool(
                "ena_init.py",
                "--home", home,
                "--timezone", "Etc/UTC",
                "--language", "en-US",
                "--recovery", "git-revert",
                "--rescuer", "operator-console",
                "--rescuer-type", "human",
            )
            self.assertEqual(created.returncode, 0, created.stdout + created.stderr)

            system_path = home / "SYSTEM.yaml"
            text = system_path.read_text(encoding="utf-8")
            text = text.replace("minimum_ready: false", "minimum_ready: true", 1)
            text = text.replace(
                "recovery:\n  primary: git-revert\n",
                "recovery:\n  primary: git-revert\n  verification_confidence: SELF_ASSERTED\n",
                1,
            )
            system_path.write_text(text, encoding="utf-8")

            preflight = self.run_tool("ena_preflight.py", "--home", home)
            self.assertEqual(preflight.returncode, 2, preflight.stdout + preflight.stderr)
            self.assertNotIn("pre-provenance READY home", preflight.stdout)
            self.assertIn("recovery.verification_evidence is missing", preflight.stdout)
            self.assertIn("recovery.verified_at is missing", preflight.stdout)


if __name__ == "__main__":
    unittest.main()
