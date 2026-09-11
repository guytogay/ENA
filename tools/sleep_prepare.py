#!/usr/bin/env python3
"""Prepare a bounded Sleep input bundle from JSONL experience and memory records."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def read_jsonl(path: str):
    p = Path(path)
    if not p.exists():
        return []
    return [json.loads(line) for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--experience", required=True)
    p.add_argument("--memory", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--max-experience", type=int, default=50)
    p.add_argument("--max-memory", type=int, default=80)
    args = p.parse_args()

    experience = read_jsonl(args.experience)[-args.max_experience :]
    memory = read_jsonl(args.memory)[-args.max_memory :]

    bundle = {
        "task": "sleep_consolidation",
        "instructions": [
            "Find repetition, duplication, fragmentation, conflict, staleness, overreach, reusable procedures, boundaries, unresolved questions, and missing links.",
            "Produce a consolidation plan before changing durable memory.",
            "Preserve provenance, counterexamples, and uncertainty.",
            "Prefer no change or a narrower memory when evidence is ambiguous.",
        ],
        "experience": experience,
        "memory": memory,
    }
    Path(args.output).write_text(json.dumps(bundle, indent=2, ensure_ascii=False), encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
