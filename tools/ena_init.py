#!/usr/bin/env python3
"""Create a minimal ENA home using only the Python standard library."""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--home", default="~/.ena")
    p.add_argument("--timezone", required=True, help="Confirmed IANA timezone, e.g. Europe/Rome")
    p.add_argument("--language", required=True, help="Confirmed language tag, e.g. en-US")
    p.add_argument(
        "--system-valid-hours",
        type=int,
        default=168,
        help="Initial SYSTEM.yaml freshness window; default 168 hours (7 days)",
    )
    args = p.parse_args()

    if args.system_valid_hours <= 0:
        raise SystemExit("--system-valid-hours must be > 0")

    tz = ZoneInfo(args.timezone)
    home = Path(args.home).expanduser().resolve()
    for rel in (
        "changes",
        "evolution/experience",
        "evolution/candidates/speculative",
        "evolution/candidates/selected",
        "evolution/runs/sleep",
        "evolution/runs/dream",
        "evolution/locks",
    ):
        (home / rel).mkdir(parents=True, exist_ok=True)

    config = home / "ENA.yaml"
    system = home / "SYSTEM.yaml"
    for path in (config, system):
        if path.exists():
            raise SystemExit(f"Refusing to overwrite existing {path}")

    config.write_text(
        "schema_version: '0.2'\n"
        f"ena_home: {home}\n"
        f"canonical_timezone: {args.timezone}\n"
        f"canonical_language: {args.language}\n"
        "text_encoding: UTF-8\n"
        "\ncommunication:\n"
        "  human: UNKNOWN\n"
        "  a2a:\n"
        "    agent_card: UNKNOWN\n"
        "    rescue_peers: []\n"
        "\nrecovery:\n"
        f"  changes: {home / 'changes'}\n"
        "  rollback_scheduler: UNKNOWN\n"
        "  backup_or_snapshot: UNKNOWN\n"
        "\nevolution:\n"
        f"  records: {home / 'evolution'}\n"
        f"  experience_inbox: {home / 'evolution/experience'}\n"
        f"  speculative_candidates: {home / 'evolution/candidates/speculative'}\n"
        f"  selected_candidates: {home / 'evolution/candidates/selected'}\n",
        encoding="utf-8",
    )

    checked = datetime.now(tz)
    valid_until = checked + timedelta(hours=args.system_valid_hours)
    system.write_text(
        "schema_version: '0.2'\n"
        f"checked_at: {checked.isoformat()}\n"
        f"valid_until: {valid_until.isoformat()}\n"
        "minimum_ready: false\n"
        f"canonical_timezone: {args.timezone}\n"
        "runtime:\n"
        "  host: UNKNOWN\n"
        "  agent_runtime: UNKNOWN\n"
        "  startup: UNKNOWN\n"
        "  restart: UNKNOWN\n"
        "  supervision: UNKNOWN\n"
        "communication:\n"
        "  human: UNKNOWN\n"
        "  a2a_agent_card: UNKNOWN\n"
        "recovery:\n"
        "  primary: UNKNOWN\n"
        "  backup_or_snapshot: UNKNOWN\n"
        "  scheduler_or_timer: UNKNOWN\n"
        "rescue:\n"
        "  primary: UNKNOWN\n"
        "  type: UNKNOWN\n"
        "memory:\n"
        "  sources: []\n"
        "  durable_store: UNKNOWN\n"
        "  retrieval_or_index: UNKNOWN\n"
        "  write_method: UNKNOWN\n"
        "change_surfaces: []\n"
        "unknowns: []\n",
        encoding="utf-8",
    )

    print(config)
    print(system)
    print("First Use is not complete yet: fill recovery/rescue facts and set minimum_ready: true.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
