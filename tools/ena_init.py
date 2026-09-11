#!/usr/bin/env python3
"""Create a minimal ENA home using only the Python standard library."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--home", default="~/.ena")
    p.add_argument("--timezone", required=True, help="IANA timezone, e.g. Asia/Shanghai")
    p.add_argument("--language", required=True, help="Language tag, e.g. zh-CN")
    args = p.parse_args()

    tz = ZoneInfo(args.timezone)
    home = Path(args.home).expanduser().resolve()
    for rel in (
        "changes",
        "evolution/experience",
        "evolution/candidates",
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
        "schema_version: '0.1'\n"
        f"ena_home: {home}\n"
        f"canonical_timezone: {args.timezone}\n"
        f"canonical_language: {args.language}\n"
        "text_encoding: UTF-8\n"
        "\ncommunication:\n"
        "  human: null\n"
        "  a2a:\n"
        "    agent_card: null\n"
        "    rescue_peers: []\n"
        "\nrecovery:\n"
        f"  changes: {home / 'changes'}\n"
        "  rollback_scheduler: null\n"
        "  backup_or_snapshot: null\n"
        "\nevolution:\n"
        f"  records: {home / 'evolution'}\n"
        f"  experience_inbox: {home / 'evolution/experience'}\n"
        f"  candidates: {home / 'evolution/candidates'}\n",
        encoding="utf-8",
    )

    now = datetime.now(tz).isoformat()
    system.write_text(
        "schema_version: '0.1'\n"
        f"inspected_at: {now}\n"
        f"canonical_timezone: {args.timezone}\n"
        "runtime:\n"
        "  host: null\n"
        "  agent_runtime: null\n"
        "  startup: null\n"
        "  restart: null\n"
        "communication:\n"
        "  human: null\n"
        "  a2a_agent_card: null\n"
        "memory:\n"
        "  sources: []\n"
        "  durable_store: null\n"
        "  retrieval_or_index: null\n"
        "  write_method: null\n"
        "recovery:\n"
        "  backup_or_snapshot: null\n"
        "  scheduler_or_timer: null\n"
        "change_surfaces: []\n"
        "unknowns: []\n",
        encoding="utf-8",
    )

    print(config)
    print(system)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
