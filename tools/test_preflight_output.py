#!/usr/bin/env python3
"""Regression tests for the home identity shown by preflight."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
TOOLS = REPO / "tools"


class PreflightOutputTests(unittest.TestCase):
    def run_tool(self, name: str, *args, env=None):
        return subprocess.run(
            [sys.executable, str(TOOLS / name), *map(str, args)],
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            env=env,
        )

    def test_default_refresh_required_names_the_resolved_default_home(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            env = os.environ.copy()
            env["HOME"] = tmpdir
            env["USERPROFILE"] = tmpdir
            expected = (Path(tmpdir) / ".ena").resolve()

            result = self.run_tool("ena_preflight.py", env=env)

            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertEqual(result.stdout.splitlines()[0], "ENA preflight: REFRESH REQUIRED")
            self.assertIn(f"Checked home: {expected}", result.stdout)

    def test_ok_names_the_resolved_checked_home(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            home = Path(tmpdir) / "ready-home"
            init = self.run_tool(
                "ena_init.py",
                "--home", home,
                "--timezone", "Etc/UTC",
                "--language", "en-US",
                "--host-profile", "session",
                "--recovery", "git-revert",
                "--recovery-evidence", "restore-check",
                "--rescuer", "human-operator",
                "--rescuer-evidence", "rescuer-check",
                "--rescuer-type", "human",
                "--verified-minimum",
            )
            self.assertEqual(init.returncode, 0, init.stdout + init.stderr)

            result = self.run_tool("ena_preflight.py", "--home", home)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(result.stdout.splitlines()[0], "ENA preflight: OK")
            self.assertIn(f"Checked home: {home.resolve()}", result.stdout)


if __name__ == "__main__":
    unittest.main()
