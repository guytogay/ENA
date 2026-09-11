#!/usr/bin/env python3
"""Run a local smoke test of the ENA reference tools without touching live Agent state."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


def raw(*args):
    return subprocess.run([sys.executable, *map(str, args)], text=True, capture_output=True)


def run(*args):
    result = raw(*args)
    if result.returncode:
        raise SystemExit(result.stdout + result.stderr)
    return result.stdout.strip()


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    tools = repo / "tools"
    examples = repo / "examples" / "evolution"

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        home = tmp / "ena-home"
        run(tools / "ena_init.py", "--home", home, "--timezone", "Etc/UTC", "--language", "en-US")
        assert (home / "ENA.yaml").is_file()
        system = home / "SYSTEM.yaml"
        assert system.is_file()

        preflight = raw(tools / "ena_preflight.py", "--home", home)
        assert preflight.returncode == 2
        assert "REFRESH REQUIRED" in preflight.stdout

        text = system.read_text(encoding="utf-8")
        text = text.replace("minimum_ready: false", "minimum_ready: true")
        text = text.replace("  primary: UNKNOWN\n  backup_or_snapshot", "  primary: git-revert\n  backup_or_snapshot", 1)
        text = text.replace("rescue:\n  primary: UNKNOWN\n  type: UNKNOWN", "rescue:\n  primary: human-operator\n  type: human")
        system.write_text(text, encoding="utf-8")
        run(tools / "ena_preflight.py", "--home", home)

        package = run(tools / "change_scaffold.py", "--home", home, "--timezone", "Etc/UTC", "--name", "self-test")
        assert Path(package).is_dir()

        sleep_out = tmp / "sleep-input.json"
        run(
            tools / "sleep_prepare.py",
            "--experience", examples / "EXPERIENCE.example.jsonl",
            "--memory", examples / "MEMORY.example.jsonl",
            "--output", sleep_out,
        )
        assert json.loads(sleep_out.read_text(encoding="utf-8"))["task"] == "sleep_consolidation"

        dream_out = tmp / "dream-set.json"
        run(
            tools / "dream_sample.py",
            "--memory", examples / "MEMORY.example.jsonl",
            "--output", dream_out,
            "--seed", "42",
        )
        dream = json.loads(dream_out.read_text(encoding="utf-8"))
        assert dream["truth_status"] == "speculative_input"
        assert len(dream["fragments"]) >= 2

        candidate_path = Path(run(
            tools / "candidate_record.py",
            "--home", home,
            "--origin", "dream",
            "--candidate", "Try a different recovery sequence",
            "--reality-check", "Compare against one bounded real task",
        ))
        candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
        assert candidate["truth_status"] == "speculative"
        assert candidate_path.parent.name == "speculative"

    print("ENA reference tools: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
