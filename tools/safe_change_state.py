#!/usr/bin/env python3
"""Validate and advance the SAFE-CHANGE state machine."""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

from control_yaml import missing, scalar
from ena_home import EnaHomeError, home_of_package, read_control, require_initialized_home
from ena_text import read_text


ALLOWED = {
    "preparing": {"armed", "cancelled"},
    "armed": {"applied", "cancelled"},
    "applied": {"retained", "restoring"},
    "restoring": {"restored", "failed"},
    "retained": set(),
    "restored": set(),
    "failed": set(),
    "cancelled": set(),
}

REQUIRED_FOR_ARM = (
    "host_profile",
    "target",
    "recovery_actor",
    "where_to_act",
    "changed",
    "known_good",
    "rollback_action",
    "restart_or_new_session",
    "verify_operation",
)

PLACEHOLDER_MARKER = "UNCONFIGURED_ROLLBACK"
ROLLBACK_EXECUTABLE = "executable_script"
ROLLBACK_DECLARED_MANUAL = "declared_no_automatic_rollback"

ROLLBACK_DESCRIPTIONS = {
    "placeholder": "rollback.py is still the unconfigured placeholder",
    "absent": "the package has no rollback.py",
    "unreadable": "rollback.py cannot be read",
}

ROLLBACK_CLAIM_CONFLICTS = {
    "placeholder": "rollback_action points at rollback.py, which is still the unconfigured placeholder",
    "absent": "rollback_action points at rollback.py, but the package has no rollback.py",
    "unreadable": "rollback_action points at rollback.py, which cannot be read",
}


def rollback_state(package: Path) -> str:
    """Report what the package can actually execute right now."""
    script = package / "rollback.py"
    if not script.is_file():
        return "absent"
    try:
        text = read_text(script)
    except (OSError, UnicodeError):
        return "unreadable"
    return "placeholder" if PLACEHOLDER_MARKER in text else "executable"


def rollback_problems(rescue: dict[str, object], state: str) -> tuple[list[str], str | None]:
    """Require the recovery declaration to match what the package can execute.

    `tools/README.md` and `SAFE-CHANGE.md` both say the scaffolded `rollback.py`
    must be replaced *or* a verified Host-native recovery action recorded before
    arming. The gate previously checked only that `rollback_action` was non-empty
    and, additionally, only when that text happened to contain the literal
    `rollback.py`, so an undeclared placeholder reached `armed`, `applied` and
    `retained` looking exactly like prepared recovery.
    """
    problems: list[str] = []
    declared = scalar(rescue, "automatic_rollback")
    mode: str | None = None

    if state == "executable":
        mode = ROLLBACK_EXECUTABLE
    else:
        description = ROLLBACK_DESCRIPTIONS.get(state, "rollback.py is not executable")
        if missing(declared):
            problems.append(
                f"{description}: provide an executable rollback or declare automatic_rollback: false "
                "to record that rollback is manual/Host-native"
            )
        elif declared.strip().lower() == "true":
            problems.append(f"rescue.yaml automatic_rollback is true but {description}")
        else:
            mode = ROLLBACK_DECLARED_MANUAL

    rollback_action = scalar(rescue, "rollback_action") or ""
    if "rollback.py" in rollback_action and state in ROLLBACK_CLAIM_CONFLICTS:
        problems.append(ROLLBACK_CLAIM_CONFLICTS[state])

    return problems, mode


def write_status(
    path: Path, state: str, profile: str, previous: str, evidence: str | None, tz, tz_name: str
) -> str:
    now = datetime.now(tz).isoformat(timespec="seconds")
    text = (
        "schema_version: '0.3'\n"
        f"host_profile: {profile}\n"
        f"state: {state}\n"
        f"updated_at: {now}\n"
        f"previous_state: {previous}\n"
        f"last_evidence: {evidence if evidence else 'null'}\n"
        f"timezone: {tz_name}\n"
    )
    temp = path.with_suffix(".yaml.tmp")
    temp.write_text(text, encoding="utf-8")
    os.replace(temp, path)
    return now


def main() -> int:
    p = argparse.ArgumentParser(description="Gate one SAFE-CHANGE state transition.")
    p.add_argument("package", type=Path)
    p.add_argument("to_state", choices=tuple(ALLOWED))
    p.add_argument("--evidence", help="Required for retained/restored/failed")
    args = p.parse_args()

    package = args.package.expanduser().resolve()
    status_path = package / "status.yaml"
    rescue_path = package / "rescue.yaml"
    if not status_path.is_file() or not rescue_path.is_file():
        print("SAFE-CHANGE gate: missing status.yaml or rescue.yaml", file=sys.stderr)
        return 2

    try:
        tz, tz_name = require_initialized_home(home_of_package(package))
    except EnaHomeError as exc:
        print(f"SAFE-CHANGE gate: {exc}", file=sys.stderr)
        return 2

    try:
        status = read_control(status_path)
        rescue = read_control(rescue_path)
    except EnaHomeError as exc:
        print(f"SAFE-CHANGE gate: {exc}", file=sys.stderr)
        return 2

    current = scalar(status, "state")
    profile = scalar(status, "host_profile")
    if current not in ALLOWED:
        print(f"SAFE-CHANGE gate: invalid current state {current!r}", file=sys.stderr)
        return 2
    if args.to_state not in ALLOWED[current]:
        print(f"SAFE-CHANGE gate: transition {current} -> {args.to_state} is not allowed", file=sys.stderr)
        return 2

    problems: list[str] = []
    rollback_mode: str | None = None
    if args.to_state == "armed":
        if profile not in {"resident", "session"}:
            problems.append("status.yaml host_profile must be resident or session")
        if scalar(rescue, "host_profile") != profile:
            problems.append("rescue.yaml host_profile must match status.yaml")
        for key in REQUIRED_FOR_ARM:
            if missing(scalar(rescue, key)):
                problems.append(f"rescue.yaml {key} is unresolved")

        recovery_problems, rollback_mode = rollback_problems(rescue, rollback_state(package))
        problems.extend(recovery_problems)

    if args.to_state in {"retained", "restored", "failed"} and not args.evidence:
        problems.append(f"{args.to_state} requires --evidence")

    if problems:
        print("SAFE-CHANGE gate: BLOCKED", file=sys.stderr)
        for item in problems:
            print(f"- {item}", file=sys.stderr)
        return 2

    now = write_status(
        status_path,
        args.to_state,
        profile or "UNKNOWN",
        current,
        args.evidence,
        tz,
        tz_name,
    )
    transition = {
        "at": now,
        "from": current,
        "to": args.to_state,
        "evidence": args.evidence,
        "timezone": tz_name,
    }
    if args.to_state == "armed":
        transition["rollback_mode"] = rollback_mode
    with (package / "transitions.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(transition) + "\n")

    print(f"SAFE-CHANGE gate: {current} -> {args.to_state}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
