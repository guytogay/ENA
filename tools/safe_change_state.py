#!/usr/bin/env python3
"""Validate and advance the SAFE-CHANGE state machine."""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from control_yaml import ControlYamlError, missing, parse_control_yaml, scalar


ALLOWED = {
    "preparing": {"armed", "cancelled"},
    "armed": {"applied", "cancelled"},
    "applied": {"retained", "restoring", "failed"},
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


def read_control(path: Path) -> dict[str, object]:
    try:
        return parse_control_yaml(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ControlYamlError) as exc:
        raise ValueError(f"{path.name}: {exc}") from exc


def write_status(path: Path, state: str, profile: str, previous: str, evidence: str | None) -> str:
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    text = (
        "schema_version: '0.3'\n"
        f"host_profile: {profile}\n"
        f"state: {state}\n"
        f"updated_at: {now}\n"
        f"previous_state: {previous}\n"
        f"last_evidence: {evidence if evidence else 'null'}\n"
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
        status = read_control(status_path)
        rescue = read_control(rescue_path)
    except ValueError as exc:
        print(f"SAFE-CHANGE gate: cannot safely parse control file: {exc}", file=sys.stderr)
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
    if args.to_state == "armed":
        if profile not in {"resident", "session"}:
            problems.append("status.yaml host_profile must be resident or session")
        if scalar(rescue, "host_profile") != profile:
            problems.append("rescue.yaml host_profile must match status.yaml")
        for key in REQUIRED_FOR_ARM:
            if missing(scalar(rescue, key)):
                problems.append(f"rescue.yaml {key} is unresolved")

    if args.to_state in {"retained", "restored", "failed"} and not args.evidence:
        problems.append(f"{args.to_state} requires --evidence")

    if problems:
        print("SAFE-CHANGE gate: BLOCKED", file=sys.stderr)
        for item in problems:
            print(f"- {item}", file=sys.stderr)
        return 2

    now = write_status(status_path, args.to_state, profile or "UNKNOWN", current, args.evidence)
    with (package / "transitions.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"at": now, "from": current, "to": args.to_state, "evidence": args.evidence}) + "\n")

    print(f"SAFE-CHANGE gate: {current} -> {args.to_state}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
