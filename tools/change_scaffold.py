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
    p.add_argument("--timezone", default="Asia/Shanghai")
    args = p.parse_args()

    now = datetime.now(ZoneInfo(args.timezone))
    stamp = now.strftime("%Y%m%dT%H%M%S%z")
    package = Path(args.home).expanduser().resolve() / "changes" / f"{stamp}__{clean(args.name)}"
    (package / "backup").mkdir(parents=True, exist_ok=False)

    (package / "status.yaml").write_text(f"state: preparing\nupdated_at: {now.isoformat()}\n", encoding="utf-8")
    (package / "change.md").write_text("# Change\n\nWhat will change:\n\nWhy:\n\nPrevious working state:\n\nRollback:\n\nVerification:\n", encoding="utf-8")
    (package / "rescue.yaml").write_text("target: null\nwhere_to_act: null\nchanged: []\nknown_good: null\nrollback_action: null\nautomatic_rollback: null\nrestart_action: null\nverify_communication: null\nfallback: null\n", encoding="utf-8")

    print(package)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
