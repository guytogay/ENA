#!/usr/bin/env python3
"""Fail when tracked repository files match known temporary/local-only signatures."""

from __future__ import annotations

import subprocess
import unittest
from pathlib import Path


ALLOWED_ENV_FILES = {".env.example", ".env.sample", ".env.template"}
BANNED_SUFFIXES = {".pyc", ".tmp", ".temp", ".bak", ".swp", ".swo", ".orig"}


def tracked_paths(repo: Path) -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=repo,
        check=True,
        capture_output=True,
    )
    return [Path(item.decode("utf-8")) for item in result.stdout.split(b"\0") if item]


def violation_reason(path: Path) -> str | None:
    name = path.name
    upper = name.upper()

    if "__pycache__" in path.parts:
        return "tracked Python bytecode cache"
    if name == ".DS_Store":
        return "tracked macOS metadata file"
    if path.suffix.lower() in BANNED_SUFFIXES or name.endswith("~"):
        return "tracked temporary/editor backup file"
    if upper == "TEMP" or upper.endswith("-TEMP") or upper.endswith("_TEMP"):
        return "tracked temporary marker file"
    if (name == ".env" or name.startswith(".env.")) and name not in ALLOWED_ENV_FILES:
        return "tracked environment file; keep secrets/local configuration out of the repository"
    return None


class RepositoryHygieneTests(unittest.TestCase):
    def test_tracked_files_do_not_match_known_local_or_temp_signatures(self):
        repo = Path(__file__).resolve().parents[1]
        violations = []
        for path in tracked_paths(repo):
            reason = violation_reason(path)
            if reason:
                violations.append(f"{path.as_posix()}: {reason}")

        self.assertFalse(
            violations,
            "repository hygiene violations:\n" + "\n".join(violations),
        )


if __name__ == "__main__":
    unittest.main()
