#!/usr/bin/env python3
"""Regression tests for fail-closed ENA initialization refusals."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
TOOLS = REPO / "tools"


class InitRefusalTests(unittest.TestCase):
    def run_tool(self, *args):
        return subprocess.run(
            [sys.executable, *map(str, args)],
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
        )

    def init_command(self, home: Path, *extra):
        return (
            TOOLS / "ena_init.py",
            "--home", home,
            "--timezone", "Etc/UTC",
            "--language", "en-US",
            "--host-profile", "session",
            *extra,
        )

    @staticmethod
    def snapshot(root: Path) -> tuple:
        if root.is_file():
            return ((".", "file", root.read_bytes()),)
        if not root.exists():
            return ()
        items = []
        for path in sorted(root.rglob("*"), key=lambda item: item.as_posix()):
            rel = path.relative_to(root).as_posix()
            if path.is_dir():
                items.append((rel, "dir", None))
            elif path.is_file():
                items.append((rel, "file", path.read_bytes()))
            else:
                items.append((rel, "other", None))
        return tuple(items)

    def test_existing_control_file_refusal_has_no_filesystem_effect(self):
        for control in ("ENA.yaml", "SYSTEM.yaml"):
            with self.subTest(control=control), tempfile.TemporaryDirectory() as tmpdir:
                home = Path(tmpdir) / "home"
                home.mkdir()
                (home / control).write_text("sentinel\n", encoding="utf-8")
                before = self.snapshot(home)

                result = self.run_tool(*self.init_command(home))

                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertIn("Refusing to overwrite existing", result.stderr)
                self.assertNotIn("Traceback", result.stdout + result.stderr)
                self.assertEqual(self.snapshot(home), before)

    def test_regular_file_home_is_a_clean_controlled_refusal(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            home = Path(tmpdir) / "home-file"
            home.write_bytes(b"not a directory\n")
            before = home.read_bytes()

            result = self.run_tool(*self.init_command(home))

            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertIn("target is not a directory", result.stderr)
            self.assertNotIn("Traceback", result.stdout + result.stderr)
            self.assertEqual(home.read_bytes(), before)

    def test_first_use_wraps_file_home_without_a_traceback(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            home = Path(tmpdir) / "home-file"
            home.write_bytes(b"not a directory\n")

            result = self.run_tool(
                TOOLS / "ena_first_use.py",
                "--home", home,
                "--timezone", "Etc/UTC",
                "--language", "en-US",
            )

            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertIn("ENA First Use: ERROR:", result.stderr)
            self.assertIn("target is not a directory", result.stderr)
            self.assertNotIn("Traceback", result.stdout + result.stderr)

    def test_absent_valid_home_still_initializes(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            home = Path(tmpdir) / "new-home"
            result = self.run_tool(*self.init_command(home))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue((home / "ENA.yaml").is_file())
            self.assertTrue((home / "SYSTEM.yaml").is_file())

    def test_all_initializer_caller_assertion_refusals_use_exit_2(self):
        cases = (
            ("valid-hours", ("--system-valid-hours", "0")),
            ("language", ("--language", "en_US")),
            ("timezone", ("--timezone", "Not/AZone")),
            ("evidence-without-verified", ("--recovery-evidence", "evidence")),
            ("verified-minimum-missing-facts", ("--verified-minimum",)),
            (
                "missing-recovery-evidence",
                (
                    "--verified-minimum",
                    "--recovery", "git-revert",
                    "--rescuer", "human-operator",
                    "--rescuer-type", "human",
                    "--rescuer-evidence", "rescuer-check",
                ),
            ),
            (
                "missing-rescuer-evidence",
                (
                    "--verified-minimum",
                    "--recovery", "git-revert",
                    "--rescuer", "human-operator",
                    "--rescuer-type", "human",
                    "--recovery-evidence", "restore-check",
                ),
            ),
        )
        for label, extra in cases:
            with self.subTest(case=label), tempfile.TemporaryDirectory() as tmpdir:
                home = Path(tmpdir) / "home"
                result = self.run_tool(*self.init_command(home, *extra))
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertNotIn("Traceback", result.stdout + result.stderr)
                self.assertFalse(home.exists(), "caller-assertion refusal must happen before initialization")

        with tempfile.TemporaryDirectory() as tmpdir:
            home = Path(tmpdir) / "home"
            home.mkdir()
            (home / "ENA.yaml").write_text("sentinel\n", encoding="utf-8")
            result = self.run_tool(*self.init_command(home))
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertNotIn("Traceback", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
