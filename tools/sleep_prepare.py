#!/usr/bin/env python3
"""Prepare a bounded Sleep input bundle from JSONL experience and memory records."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def read_jsonl(path: str) -> tuple[list[object], str | None]:
    p = Path(path)
    if not p.exists():
        return [], None
    text = p.read_text(encoding="utf-8")
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    records = [json.loads(line) for line in text.splitlines() if line.strip()]
    return records, digest


def bounded_source(reference: str, role: str, max_records: int) -> tuple[list[object], dict[str, object]]:
    records, digest = read_jsonl(reference)
    selected = records[-max_records:] if max_records > 0 else []
    meta = {
        "role": role,
        "reference": reference,
        "sha256": digest,
        "source_record_count": len(records),
        "selected_record_count": len(selected),
        "selection": {
            "strategy": "tail",
            "max_records": max_records,
        },
    }
    return selected, meta


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--experience", required=True)
    p.add_argument("--memory", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--max-experience", type=int, default=50)
    p.add_argument("--max-memory", type=int, default=80)
    args = p.parse_args()

    if args.max_experience < 0 or args.max_memory < 0:
        raise SystemExit("--max-experience and --max-memory must be >= 0")

    experience, experience_meta = bounded_source(args.experience, "experience", args.max_experience)
    memory, memory_meta = bounded_source(args.memory, "memory", args.max_memory)

    bundle = {
        "task": "sleep_consolidation",
        "input": {
            "prepared_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
            "sources": [experience_meta, memory_meta],
        },
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
