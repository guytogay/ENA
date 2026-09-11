#!/usr/bin/env python3
"""Create a minimal ENA home using only the Python standard library."""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo


def known(value: str | None) -> bool:
    return bool(value and value.strip() and value.strip().upper() != "UNKNOWN")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--home", default="~/.ena")
    p.add_argument("--timezone", required=True, help="Confirmed/pre-provisioned IANA timezone")
    p.add_argument("--language", required=True, help="Confirmed/pre-provisioned language tag")
    p.add_argument("--host-profile", choices=("resident", "session"), default="UNKNOWN")
    p.add_argument("--recovery", default="UNKNOWN", help="Verified external recovery path/reference")
    p.add_argument("--rescuer", default="UNKNOWN", help="Verified human/Agent/Host recovery actor")
    p.add_argument("--rescuer-type", choices=("human", "agent", "host", "UNKNOWN"), default="UNKNOWN")
    p.add_argument(
        "--verified-minimum",
        action="store_true",
        help="Mark minimum_ready only when the supplied recovery/rescuer values were already verified by the caller",
    )
    p.add_argument(
        "--system-valid-hours",
        type=int,
        default=168,
        help="Initial SYSTEM.yaml freshness window; default 168 hours (7 days)",
    )
    args = p.parse_args()

    if args.system_valid_hours <= 0:
        raise SystemExit("--system-valid-hours must be > 0")

    if args.verified_minimum and not (
        known(args.recovery) and known(args.rescuer) and args.rescuer_type != "UNKNOWN"
    ):
        raise SystemExit(
            "--verified-minimum requires non-UNKNOWN --recovery, --rescuer and --rescuer-type"
        )

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
        "\nsurvival:\n"
        f"  host_profile: {args.host_profile}\n"
        f"  external_escalation: {args.rescuer}\n"
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
    ready = "true" if args.verified_minimum else "false"
    system.write_text(
        "schema_version: '0.2'\n"
        f"checked_at: {checked.isoformat()}\n"
        f"valid_until: {valid_until.isoformat()}\n"
        f"minimum_ready: {ready}\n"
        f"canonical_timezone: {args.timezone}\n"
        "runtime:\n"
        "  host: UNKNOWN\n"
        "  agent_runtime: UNKNOWN\n"
        f"  host_profile: {args.host_profile}\n"
        "  startup: UNKNOWN\n"
        "  restart: UNKNOWN\n"
        "  supervision: UNKNOWN\n"
        "communication:\n"
        "  human: UNKNOWN\n"
        "  a2a_agent_card: UNKNOWN\n"
        "recovery:\n"
        f"  primary: {args.recovery}\n"
        "  backup_or_snapshot: UNKNOWN\n"
        "  scheduler_or_timer: UNKNOWN\n"
        "rescue:\n"
        f"  primary: {args.rescuer}\n"
        f"  type: {args.rescuer_type}\n"
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
    if args.verified_minimum:
        print("Minimum First Use recorded from caller-verified preset values.")
    else:
        print("First Use is not complete yet: verify recovery/rescue facts and set minimum_ready: true.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
