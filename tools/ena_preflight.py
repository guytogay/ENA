#!/usr/bin/env python3
"""Fail fast when ENA First Use is missing, incomplete or stale."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path


def clean(value: str) -> str:
    return value.strip().strip("'\"")


def root_scalar(text: str, key: str) -> str | None:
    prefix = f"{key}:"
    for line in text.splitlines():
        if line.startswith(prefix):
            return clean(line[len(prefix):])
    return None


def child_scalar(text: str, section: str, key: str) -> str | None:
    lines = text.splitlines()
    section_line = f"{section}:"
    child_prefix = f"  {key}:"
    inside = False
    for line in lines:
        if not line.startswith(" "):
            inside = line == section_line
            continue
        if inside and line.startswith(child_prefix):
            return clean(line[len(child_prefix):])
    return None


def missing_value(value: str | None) -> bool:
    return value is None or value.lower() in {"", "unknown", "null", "none", "~"}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--home", default="~/.ena")
    args = p.parse_args()

    home = Path(args.home).expanduser().resolve()
    config = home / "ENA.yaml"
    system = home / "SYSTEM.yaml"

    problems: list[str] = []
    if not config.exists():
        problems.append(f"missing {config}")
    if not system.exists():
        problems.append(f"missing {system}")

    if system.exists():
        text = system.read_text(encoding="utf-8")
        ready = (root_scalar(text, "minimum_ready") or "").lower()
        if ready != "true":
            problems.append("SYSTEM.yaml minimum_ready is not true")

        recovery = child_scalar(text, "recovery", "primary")
        if missing_value(recovery):
            problems.append("SYSTEM.yaml has no real recovery.primary")

        rescuer = child_scalar(text, "rescue", "primary")
        if missing_value(rescuer):
            problems.append("SYSTEM.yaml has no real rescue.primary")

        valid_until = root_scalar(text, "valid_until")
        if not valid_until:
            problems.append("SYSTEM.yaml has no valid_until")
        else:
            try:
                deadline = datetime.fromisoformat(valid_until.replace("Z", "+00:00"))
                if deadline.tzinfo is None:
                    problems.append("SYSTEM.yaml valid_until must include a timezone offset")
                elif datetime.now(deadline.tzinfo) > deadline:
                    problems.append(f"SYSTEM.yaml expired at {deadline.isoformat()}")
            except ValueError:
                problems.append("SYSTEM.yaml valid_until is not a valid ISO-8601 timestamp")

    if problems:
        print("ENA preflight: REFRESH REQUIRED")
        for item in problems:
            print(f"- {item}")
        print("Apply FIRST-USE.md before ordinary work.")
        return 2

    print("ENA preflight: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
