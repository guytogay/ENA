#!/usr/bin/env python3
"""Create a timestamped SAFE-CHANGE package using only the standard library."""

from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path

from timezone_utils import TimezoneUnavailable, load_timezone


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

    try:
        tz = load_timezone(args.timezone)
    except TimezoneUnavailable as exc:
        raise SystemExit(str(exc)) from exc

    now = datetime.now(tz)
    stamp = now.strftime("%Y%m%dT%H%M%S%z")
    package = Path(args.home).expanduser().resolve() / "changes" / f"{stamp}__{clean(args.name)}"
    (package / "backup").mkdir(parents=True, exist_ok=False)

    (package / "status.yaml").write_text(
        "schema_version: '0.3'\n"
        f"host_profile: {args.profile}\n"
        "state: preparing\n"
        f"updated_at: {now.isoformat()}\n"
        "previous_state: null\n"
        "last_evidence: null\n",
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
        "Incremental deterministic checks:\n\n"
        "Validation event references:\n\n"
        "Final verification:\n",
        encoding="utf-8",
    )
    (package / "rescue.yaml").write_text(
        "schema_version: '0.3'\n"
        f"host_profile: {args.profile}\n"
        "target: UNKNOWN\n"
        "recovery_actor: UNKNOWN\n"
        "where_to_act: UNKNOWN\n"
        "changed: UNKNOWN\n"
        "known_good: UNKNOWN\n"
        "rollback_action: UNKNOWN\n"
        "automatic_rollback: null\n"
        "restart_or_new_session: UNKNOWN\n"
        "verify_operation: UNKNOWN\n"
        "verify_communication: UNKNOWN\n"
        "restore_only: UNKNOWN\n"
        "fallback: UNKNOWN\n",
        encoding="utf-8",
    )
    (package / "rollback.py").write_text(
        "#!/usr/bin/env python3\n"
        "raise SystemExit('UNCONFIGURED_ROLLBACK: replace this placeholder or use a verified Host-native rollback action')\n",
        encoding="utf-8",
    )

    print(package)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
