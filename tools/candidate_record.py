#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--home", default="~/.ena")
    p.add_argument("--origin", required=True, choices=("dream", "sleep", "work", "other"))
    p.add_argument("--candidate", required=True)
    p.add_argument("--reality-check", required=True)
    p.add_argument("--source", action="append", default=[])
    args = p.parse_args()

    home = Path(args.home).expanduser().resolve()
    out_dir = home / "evolution" / "candidates" / "speculative"
    out_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.now().astimezone()
    target = out_dir / f"{now.strftime('%Y%m%dT%H%M%S%z')}__candidate.json"
    record = {
        "schema_version": "0.1",
        "created_at": now.isoformat(),
        "origin": args.origin,
        "truth_status": "speculative",
        "source_fragments": args.source,
        "candidate": args.candidate,
        "reality_check": args.reality_check,
        "outcome": None,
    }
    target.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
