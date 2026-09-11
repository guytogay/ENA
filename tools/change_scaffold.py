#!/usr/bin/env python3
"""Create an empty timestamped safe-change package using only the standard library."""

from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


def clean(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip()).strip("-")
    return value or "change"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--name", required=True)
    p.add_argument("--home", default="~/.ena")
    p.add_argument("--timezone", required=True, help="Confirmed IANA timezone")
    p.add_argument("--profile", choices=("resident", "session"), required=True)
    args = p.parse_args()

    now = datetime.now(ZoneInfo(args.timezone))
    stamp = now.strftime("%Y%m%dT%H%M%S%z")
    package = Path(args.home).expanduser().resolve() / "changes" / f"{stamp}__{clean(args.name)}"
    (package / "backup").mkdir(parents=True, exist_ok=False)

    (package / "status.yaml").write_text(
        f"state: preparing\nhost_profile: {args.profile}\nupdated_at: {now.isoformat()}\n",
        encoding="utf-8",
    )
    (package / "change.md").write_text(
        "# Change\n\n"
        f"Host profile: {args.profile}\n\n"
        "What will change:\n\n"
        "Why:\n\n"
        "Previous working state:\n\n"
        "Recovery actor/path:\n\n"
        "Rollback:\n\n"
        "Verification:\n",
        encoding="utf-8",
    )
    (package / "rescue.yaml").write_text(
        f"host_profile: {args.profile}\n"
        "target: UNKNOWN\n"
        "recovery_actor: UNKNOWN\n"
        "where_to_act: UNKNOWN\n"
        "changed: []\n"
        "known_good: UNKNOWN\n"
        "rollback_action: UNKNOWN\n"
        "automatic_rollback: null\n"
        "restart_or_new_session: UNKNOWN\n"
        "verify_operation: UNKNOWN\n"
        "verify_communication: UNKNOWN\n"
        "fallback: UNKNOWN\n",
        encoding="utf-8",
    )

    print(package)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
