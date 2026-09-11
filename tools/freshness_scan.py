#!/usr/bin/env python3
"""Report fresh/stale/unknown records from JSONL sources without inventing a universal TTL."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from jsonl_source import JsonlSourceError, load_jsonl_source


def parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def main() -> int:
    p = argparse.ArgumentParser(
        description="Classify JSONL records as fresh/stale/unknown from explicit freshness metadata."
    )
    p.add_argument("--input", action="append", required=True, type=Path, help="JSONL source; repeatable")
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--now", help="ISO timestamp for reproducible runs; defaults to current UTC time")
    p.add_argument(
        "--max-age-hours",
        type=float,
        help="Optional caller policy used only when checked_at exists but valid_until does not",
    )
    p.add_argument("--fail-on-stale", action="store_true")
    args = p.parse_args()

    now = parse_time(args.now) if args.now else datetime.now(timezone.utc)
    if now is None:
        p.error("--now must be an ISO timestamp")

    results = []
    counts = {"fresh": 0, "stale": 0, "unknown": 0}

    try:
        sources = [(path, load_jsonl_source(path)) for path in args.input]
    except JsonlSourceError as exc:
        print(f"ENA freshness scan: ERROR: {exc}", file=sys.stderr)
        return 2

    for path, source in sources:
        for line_no, record in enumerate(source.records, start=1):
            if not isinstance(record, dict):
                print(
                    f"ENA freshness scan: ERROR: record {line_no} in {path} must be a JSON object",
                    file=sys.stderr,
                )
                return 2
            checked_at = parse_time(record.get("checked_at"))
            valid_until = parse_time(record.get("valid_until"))

            if valid_until is not None:
                freshness = "fresh" if now <= valid_until else "stale"
                reason = "explicit_valid_until"
            elif checked_at is not None and args.max_age_hours is not None:
                freshness = "fresh" if now <= checked_at + timedelta(hours=args.max_age_hours) else "stale"
                reason = "caller_max_age"
            else:
                freshness = "unknown"
                reason = "no_explicit_freshness_policy"

            counts[freshness] += 1
            results.append(
                {
                    "id": record.get("id"),
                    "source_file": str(path),
                    "line": line_no,
                    "source_ref": record.get("source_ref"),
                    "state": record.get("state"),
                    "checked_at": record.get("checked_at"),
                    "valid_until": record.get("valid_until"),
                    "freshness": freshness,
                    "reason": reason,
                }
            )

    report = {
        "scanned_at": now.isoformat(timespec="seconds"),
        "policy": {"max_age_hours": args.max_age_hours},
        "counts": counts,
        "records": results,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(args.output)

    if args.fail_on_stale and counts["stale"]:
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
