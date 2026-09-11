#!/usr/bin/env python3
"""Combine memory, knowledge and capability JSONL into one Dream input file."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def read_jsonl(path: str, material_type: str):
    records = []
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        item = json.loads(raw)
        item.setdefault("material_type", material_type)
        records.append(item)
    return records


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--memory", required=True)
    p.add_argument("--knowledge")
    p.add_argument("--capabilities")
    p.add_argument("--output", required=True)
    args = p.parse_args()

    records = read_jsonl(args.memory, "memory")
    if args.knowledge:
        records.extend(read_jsonl(args.knowledge, "knowledge"))
    if args.capabilities:
        records.extend(read_jsonl(args.capabilities, "capability"))

    seen = set()
    for item in records:
        record_id = item.get("id")
        if not record_id:
            raise SystemExit("Every Dream material record needs an id")
        if record_id in seen:
            raise SystemExit(f"Duplicate Dream material id: {record_id}")
        seen.add(record_id)

    out = Path(args.output)
    out.write_text(
        "".join(json.dumps(item, ensure_ascii=False) + "\n" for item in records),
        encoding="utf-8",
    )
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
