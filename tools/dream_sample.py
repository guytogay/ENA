#!/usr/bin/env python3
"""Sample a Dream set from JSONL memory records using simple biased randomness."""

from __future__ import annotations

import argparse
import json
import random
from datetime import datetime
from pathlib import Path


def parse_time(value: str | None) -> float:
    if not value:
        return 0.0
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return 0.0


def choose(pool, used, rng):
    options = [x for x in pool if x.get("id") not in used]
    if not options:
        return None
    item = rng.choice(options)
    used.add(item.get("id"))
    return item


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--memory", required=True, help="JSONL records")
    p.add_argument("--output", required=True)
    p.add_argument("--seed", type=int)
    p.add_argument("--count", type=int, default=6)
    args = p.parse_args()

    rng = random.Random(args.seed)
    records = [json.loads(line) for line in Path(args.memory).read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(records) < 2:
        raise SystemExit("Need at least two memory records")

    by_time = sorted(records, key=lambda x: parse_time(x.get("timestamp")))
    quarter = max(1, len(records) // 4)
    old = by_time[:quarter]
    recent = by_time[-quarter:]
    underused = sorted(records, key=lambda x: x.get("retrieval_count", 0))[:quarter]
    unresolved = [x for x in records if x.get("unresolved")]
    external = [x for x in records if x.get("source_type") in {"user", "document", "a2a", "external"}]
    salient = sorted(records, key=lambda x: x.get("salience", 0), reverse=True)[:quarter]

    used = set()
    selected = []
    for label, pool in (
        ("recent", recent),
        ("old", old),
        ("underused", underused),
        ("external_or_unresolved", unresolved or external),
        ("salient", salient),
        ("random", records),
    ):
        if len(selected) >= args.count:
            break
        item = choose(pool, used, rng)
        if item is not None:
            selected.append({"pool": label, "memory": item})

    while len(selected) < min(args.count, len(records)):
        item = choose(records, used, rng)
        if item is None:
            break
        selected.append({"pool": "random", "memory": item})

    Path(args.output).write_text(json.dumps({"truth_status": "speculative_input", "fragments": selected}, indent=2, ensure_ascii=False), encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
