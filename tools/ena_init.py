#!/usr/bin/env python3
"""Create a minimal ENA home using only the Python standard library."""

from __future__ import annotations

import argparse
from pathlib import Path
from zoneinfo import ZoneInfo


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--home", default="~/.ena")
    p.add_argument("--timezone", required=True, help="IANA timezone, e.g. Asia/Shanghai")
    p.add_argument("--language", required=True, help="Language tag, e.g. zh-CN")
    args = p.parse_args()

    ZoneInfo(args.timezone)  # fail early on an invalid timezone
    home = Path(args.home).expanduser().resolve()
    for rel in ("changes", "evolution/experience", "evolution/candidates", "evolution/runs/sleep", "evolution/runs/dream", "evolution/locks"):
        (home / rel).mkdir(parents=True, exist_ok=True)

    config = home / "ENA.yaml"
    if config.exists():
        raise SystemExit(f"Refusing to overwrite existing {config}")

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

    print(config)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
