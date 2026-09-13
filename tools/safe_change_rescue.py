#!/usr/bin/env python3
"""Validate explicit SAFE-CHANGE rescue declarations used at the armed boundary."""

from __future__ import annotations

import re

from control_yaml import missing, scalar

RESCUE_SCHEMA_VERSION = "0.4"
NOT_NEEDED = "NOT_NEEDED"
CONTROL_DECLARATION_TOKENS = {
    "UNKNOWN",
    "STALLED_UNKNOWN",
    "UNAVAILABLE",
    "NOT_NEEDED",
    "NOT_APPLICABLE",
    "DEFERRED",
}
EXACT_BOOLEAN_VALUES = {"true": True, "false": False}


def _control_token_collision(value: str) -> str | None:
    """Detect near spellings of existing ENA control tokens without accepting them as aliases."""
    candidate = re.sub(r"[\s-]+", "_", value.strip()).upper()
    if candidate in CONTROL_DECLARATION_TOKENS:
        return candidate
    return None


def _declaration_problem(value: str | None, *, allow_not_needed: bool) -> str | None:
    if missing(value):
        return "is unresolved"
    assert value is not None
    collision = _control_token_collision(value)
    if collision is not None:
        if allow_not_needed and value == NOT_NEEDED:
            return None
        if allow_not_needed:
            return f"must be a concrete declaration or exact {NOT_NEEDED}"
        return "must be a concrete declaration"
    return None


def _boolean_problem(value: str | None) -> str | None:
    if value is None or value not in EXACT_BOOLEAN_VALUES:
        return "must be exactly true or false"
    return None


def armed_rescue_declarations(rescue: dict[str, object]) -> tuple[dict[str, object], list[str]]:
    """Return the explicit declarations to preserve in the armed transition."""
    problems: list[str] = []
    recorded: dict[str, object] = {}

    if scalar(rescue, "schema_version") != RESCUE_SCHEMA_VERSION:
        problems.append(
            f"rescue.yaml schema_version must be {RESCUE_SCHEMA_VERSION}; "
            "reconcile older SAFE-CHANGE packages before arming"
        )

    for key in ("verify_communication", "fallback"):
        value = scalar(rescue, key)
        issue = _declaration_problem(value, allow_not_needed=True)
        if issue:
            problems.append(f"rescue.yaml {key} {issue}")
        else:
            recorded[key] = value

    restore_only = scalar(rescue, "restore_only")
    restore_issue = _declaration_problem(restore_only, allow_not_needed=False)
    if restore_issue:
        problems.append(f"rescue.yaml restore_only {restore_issue}")
    else:
        recorded["restore_only"] = restore_only

    path_flags: dict[str, bool] = {}
    for key in ("touches_only_communication_path", "touches_only_recovery_path"):
        raw = scalar(rescue, key)
        issue = _boolean_problem(raw)
        if issue:
            problems.append(f"rescue.yaml {key} {issue}")
        else:
            assert raw is not None
            path_flags[key] = EXACT_BOOLEAN_VALUES[raw]
            recorded[key] = EXACT_BOOLEAN_VALUES[raw]

    if (
        path_flags.get("touches_only_communication_path") is True
        and path_flags.get("touches_only_recovery_path") is True
    ):
        problems.append(
            "rescue.yaml declares that this operation touches both the only communication path "
            "and the only recovery path; establish another path or split the change before arming"
        )

    return recorded, problems
