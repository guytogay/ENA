#!/usr/bin/env python3
"""Run a local smoke test of the ENA reference tools without touching live Agent state."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


def run(*args):
    result = subprocess.run([sys.executable, *map(str, args)], text=True, capture_output=True)
    if result.returncode:
        raise SystemExit(result.stdout + result.stderr)
    return result.stdout.strip()


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    tools = repo / "tools"
    examples = repo / "examples" / "evolution"

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        home = tmp / "ena-home"
        run(tools / "ena_init.py", "--home", home, "--timezone", "Asia/Shanghai", "--language", "zh-CN")
        assert (home / "ENA.yaml").is_file()
        assert (home / "SYSTEM.yaml").is_file()

        package = run(tools / "change_scaffold.py", "--home", home, "--timezone", "Asia/Shanghai", "--name", "self-test")
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

    print("ENA reference tools: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
