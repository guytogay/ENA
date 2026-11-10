#!/usr/bin/env python3
"""Record and review sampled task-level resource use against verified outcomes.

This is an opt-in learning aid, not a quota, always-on monitor, or Agent leaderboard.
It records only task metadata and supplied evidence references, never prompts or traces.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import uuid
from collections import Counter, defaultdict
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from statistics import median

from ena_actor import actor_block, resolve_actor
from ena_home import EnaHomeError, require_initialized_home, resolve_home_path
from ena_text import read_text

OUTCOMES = ("complete", "partial", "failed", "cancelled")
QUALITY = ("verified", "not_verified", "unknown")
USAGE_SOURCES = ("host", "provider", "estimate", "mixed", "unknown")
PATTERNS = (
    "repeated-context",
    "blind-retry",
    "tool-model-mismatch",
    "handoff-rework",
    "missing-completion-check",
    "overplanning",
    "scope-change",
    "necessary-complexity",
    "unknown",
)
SLUG = re.compile(r"^[a-z0-9][a-z0-9._-]{0,63}$")
CURRENCY = re.compile(r"^[A-Z]{3}$")


def nonnegative_int(raw: str) -> int:
    try:
        value = int(raw)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be a whole number") from exc
    if value < 0:
        raise argparse.ArgumentTypeError("must be zero or greater")
    return value


def nonnegative_decimal(raw: str) -> Decimal:
    try:
        value = Decimal(raw)
    except InvalidOperation as exc:
        raise argparse.ArgumentTypeError("must be a decimal number") from exc
    if not value.is_finite() or value < 0:
        raise argparse.ArgumentTypeError("must be a finite number zero or greater")
    return value


def resource_records_dir(home: Path) -> Path:
    evolution = resolve_home_path(
        home, "evolution.records", default_relative="evolution"
    )
    root = (evolution / "resource-use").resolve()
    records = (root / "records").resolve()
    for target in (root, records):
        try:
            target.relative_to(home.resolve())
        except ValueError as exc:
            raise EnaHomeError(
                f"resource-use path resolves outside the active ENA home: {target}"
            ) from exc
    return records


def validate_label(value: str, label: str) -> str:
    value = value.strip().lower()
    if not SLUG.fullmatch(value):
        raise ValueError(
            f"{label} must be a 1–64 character lowercase label using "
            "letters, digits, dot, underscore or hyphen"
        )
    return value


def median_or_none(values: list[int | Decimal]) -> str | int | None:
    if not values:
        return None
    value = median(values)
    if isinstance(value, Decimal):
        return format(value, "f")
    return int(value) if value == int(value) else value


def token_total(usage: dict[str, object]) -> int | None:
    total = usage.get("total_tokens")
    if isinstance(total, int):
        return total
    input_tokens = usage.get("input_tokens")
    output_tokens = usage.get("output_tokens")
    if isinstance(input_tokens, int) and isinstance(output_tokens, int):
        return input_tokens + output_tokens
    return None


def record(args: argparse.Namespace) -> int:
    home = Path(args.home).expanduser().resolve()
    try:
        timezone, timezone_name = require_initialized_home(home)
        records_dir = resource_records_dir(home)
    except EnaHomeError as exc:
        print(f"ENA resource ledger: ERROR: {exc}", file=sys.stderr)
        return 2

    try:
        task_class = validate_label(args.task_class, "task-class")
        route = validate_label(args.route, "route") if args.route else "unknown"
    except ValueError as exc:
        print(f"ENA resource ledger: ERROR: {exc}", file=sys.stderr)
        return 2

    task_id = args.task_id.strip()
    if not task_id or len(task_id) > 128 or any(ord(char) < 32 for char in task_id):
        print("ENA resource ledger: ERROR: task-id must contain 1–128 characters", file=sys.stderr)
        return 2

    evidence = [item.strip() for item in args.evidence if item and item.strip()]
    if not evidence or any(len(item) > 512 or any(ord(char) < 32 for char in item) for item in evidence):
        print("ENA resource ledger: ERROR: evidence references must be non-empty, at most 512 characters, and contain no control characters", file=sys.stderr)
        return 2

    currency = args.currency.upper() if args.currency else None
    if args.cost_amount is not None and not currency:
        print("ENA resource ledger: ERROR: --currency is required with --cost-amount", file=sys.stderr)
        return 2
    if currency and not CURRENCY.fullmatch(currency):
        print("ENA resource ledger: ERROR: currency must be a three-letter code such as USD or CNY", file=sys.stderr)
        return 2
    if currency and args.cost_amount is None:
        print("ENA resource ledger: ERROR: --cost-amount is required with --currency", file=sys.stderr)
        return 2

    usage = {
        "input_tokens": args.input_tokens,
        "output_tokens": args.output_tokens,
        "total_tokens": args.total_tokens,
        "tool_calls": args.tool_calls,
        "retries": args.retries,
        "elapsed_seconds": format(args.elapsed_seconds, "f") if args.elapsed_seconds is not None else None,
        "provider_cost": format(args.cost_amount, "f") if args.cost_amount is not None else None,
        "currency": currency,
    }
    if all(value is None for key, value in usage.items() if key != "currency"):
        usage["currency"] = None

    now = datetime.now(timezone)
    record_id = f"resource-{uuid.uuid4().hex[:12]}"
    has_usage = any(value is not None for key, value in usage.items() if key != "currency")
    artifact = {
        "schema_version": "0.1",
        "id": record_id,
        "recorded_at": now.isoformat(timespec="microseconds"),
        "timezone": timezone_name,
        "task": {
            "id": task_id,
            "class": task_class,
            "route": route,
            "outcome": args.outcome,
            "quality": args.quality,
        },
        "usage_source": args.usage_source if has_usage else "unknown",
        "usage": usage,
        "suspected_patterns": sorted(set(args.pattern)),
        "evidence_refs": evidence,
        "actor": actor_block(resolve_actor()),
    }

    target = records_dir / f"{now.strftime('%Y%m%dT%H%M%S%f%z')}__{record_id}.json"
    try:
        records_dir.mkdir(parents=True, exist_ok=True)
        with target.open("x", encoding="utf-8") as stream:
            json.dump(artifact, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
    except (FileExistsError, OSError) as exc:
        print(f"ENA resource ledger: ERROR: cannot write {target}: {exc}", file=sys.stderr)
        return 2

    print(target)
    return 0


def load_records(records_dir: Path) -> list[dict[str, object]]:
    if not records_dir.exists():
        return []
    if not records_dir.is_dir():
        raise ValueError(f"resource records path is not a directory: {records_dir}")

    records: list[dict[str, object]] = []
    for path in sorted(records_dir.glob("*.json")):
        try:
            value = json.loads(read_text(path))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"cannot safely read resource record {path}: {exc}") from exc
        if not isinstance(value, dict) or value.get("schema_version") != "0.1":
            raise ValueError(f"unsupported or invalid resource record: {path}")
        task = value.get("task")
        usage = value.get("usage")
        if not isinstance(task, dict) or not isinstance(usage, dict):
            raise ValueError(f"resource record is missing task/usage objects: {path}")
        if task.get("outcome") not in OUTCOMES or task.get("quality") not in QUALITY:
            raise ValueError(f"resource record has invalid task outcome/quality: {path}")
        if not isinstance(task.get("class"), str) or not isinstance(task.get("route"), str):
            raise ValueError(f"resource record has invalid task class/route: {path}")
        try:
            validate_label(task["class"], "task-class")
            validate_label(task["route"], "route")
        except ValueError as exc:
            raise ValueError(f"resource record has invalid task class/route: {path}: {exc}") from exc
        if value.get("usage_source") not in USAGE_SOURCES:
            raise ValueError(f"resource record has invalid usage source: {path}")
        if not isinstance(value.get("evidence_refs"), list) or not value["evidence_refs"] or not all(
            isinstance(ref, str) and ref.strip() for ref in value["evidence_refs"]
        ):
            raise ValueError(f"resource record has no valid evidence references: {path}")
        patterns = value.get("suspected_patterns", [])
        if not isinstance(patterns, list) or any(pattern not in PATTERNS for pattern in patterns):
            raise ValueError(f"resource record has invalid suspected patterns: {path}")
        for field in ("input_tokens", "output_tokens", "total_tokens", "tool_calls", "retries"):
            number = usage.get(field)
            if number is not None and (not isinstance(number, int) or isinstance(number, bool) or number < 0):
                raise ValueError(f"resource record has invalid {field}: {path}")
        for field in ("elapsed_seconds", "provider_cost"):
            raw = usage.get(field)
            if raw is not None:
                try:
                    number = Decimal(raw)
                except (InvalidOperation, TypeError) as exc:
                    raise ValueError(f"resource record has invalid {field}: {path}") from exc
                if not number.is_finite() or number < 0:
                    raise ValueError(f"resource record has invalid {field}: {path}")
        currency = usage.get("currency")
        provider_cost = usage.get("provider_cost")
        if currency is not None and (not isinstance(currency, str) or not CURRENCY.fullmatch(currency)):
            raise ValueError(f"resource record has invalid currency: {path}")
        if (currency is None) != (provider_cost is None):
            raise ValueError(f"resource record must pair provider_cost with currency: {path}")
        records.append(value)
    return records


def review(args: argparse.Namespace) -> int:
    home = Path(args.home).expanduser().resolve()
    try:
        _, timezone_name = require_initialized_home(home)
        records_dir = resource_records_dir(home)
        records = load_records(records_dir)
    except (EnaHomeError, ValueError) as exc:
        print(f"ENA resource ledger: ERROR: {exc}", file=sys.stderr)
        return 2

    if args.task_class:
        try:
            selected_class = validate_label(args.task_class, "task-class")
        except ValueError as exc:
            print(f"ENA resource ledger: ERROR: {exc}", file=sys.stderr)
            return 2
        records = [item for item in records if item["task"]["class"] == selected_class]

    grouped: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for item in records:
        task = item["task"]
        grouped[(str(task["class"]), str(task["route"]))].append(item)

    summaries = []
    for (task_class, route), items in sorted(grouped.items()):
        outcomes = Counter(str(item["task"]["outcome"]) for item in items)
        verified = [
            item for item in items
            if item["task"]["outcome"] == "complete" and item["task"]["quality"] == "verified"
        ]
        other = [item for item in items if item not in verified]

        verified_tokens = [
            total for item in verified
            if (total := token_total(item["usage"])) is not None
        ]
        other_tokens = [
            total for item in other
            if (total := token_total(item["usage"])) is not None
        ]
        verified_elapsed = [
            Decimal(item["usage"]["elapsed_seconds"])
            for item in verified
            if item["usage"].get("elapsed_seconds") is not None
        ]
        verified_tool_calls = [
            item["usage"]["tool_calls"]
            for item in verified
            if isinstance(item["usage"].get("tool_calls"), int)
        ]
        sources = Counter(str(item.get("usage_source", "unknown")) for item in items)
        patterns = Counter(
            pattern
            for item in items
            for pattern in item.get("suspected_patterns", [])
            if isinstance(pattern, str)
        )

        cost_samples: dict[str, list[Decimal]] = defaultdict(list)
        for item in verified:
            usage = item["usage"]
            amount = usage.get("provider_cost")
            currency = usage.get("currency")
            if isinstance(amount, str) and isinstance(currency, str):
                try:
                    cost_samples[currency].append(Decimal(amount))
                except InvalidOperation:
                    raise ValueError(f"invalid provider cost in resource record {item.get('id')}")

        summaries.append({
            "task_class": task_class,
            "route": route,
            "records": len(items),
            "outcomes": {name: outcomes.get(name, 0) for name in OUTCOMES},
            "verified_completions": len(verified),
            "verified_completion_usage_samples": len(verified_tokens),
            "median_tokens_per_verified_completion": median_or_none(verified_tokens),
            "other_outcome_usage_samples": len(other_tokens),
            "median_tokens_per_other_outcome": median_or_none(other_tokens),
            "median_elapsed_seconds_per_verified_completion": median_or_none(verified_elapsed),
            "median_tool_calls_per_verified_completion": median_or_none(verified_tool_calls),
            "median_provider_cost_per_verified_completion": {
                currency: median_or_none(values) for currency, values in sorted(cost_samples.items())
            },
            "usage_sources": dict(sorted(sources.items())),
            "pattern_hypotheses": dict(sorted(patterns.items())),
        })

    report = {
        "schema_version": "0.1",
        "timezone": timezone_name,
        "records_reviewed": len(records),
        "task_class_filter": args.task_class,
        "groups": summaries,
        "interpretation_limits": [
            "This report describes recorded samples; it does not decide whether a high-cost task was wasteful.",
            "Compare only sufficiently similar task classes and routes; task difficulty and required quality can differ.",
            "Token medians use records with total_tokens or both input_tokens and output_tokens; sample counts are explicit.",
            "Pattern labels are hypotheses supplied by the recorder, not verified root causes.",
            "Missing usage data stays unknown; no cost or token value is inferred.",
            "The ledger stores metadata and evidence references, not prompts, private reasoning or raw tool traces.",
            "There is no per-Agent ranking, efficiency score, quota or automatic execution limit.",
        ],
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Record and review sampled task-level resource use against verified outcomes."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    add = subparsers.add_parser("record", help="record one task outcome and available usage evidence")
    add.add_argument("--home", default="~/.ena")
    add.add_argument("--task-id", required=True)
    add.add_argument("--task-class", required=True, help="comparable task category, e.g. code-fix")
    add.add_argument("--route", help="optional model/tool route label")
    add.add_argument("--outcome", required=True, choices=OUTCOMES)
    add.add_argument("--quality", default="unknown", choices=QUALITY)
    add.add_argument("--usage-source", default="unknown", choices=USAGE_SOURCES)
    add.add_argument("--input-tokens", type=nonnegative_int)
    add.add_argument("--output-tokens", type=nonnegative_int)
    add.add_argument("--total-tokens", type=nonnegative_int)
    add.add_argument("--tool-calls", type=nonnegative_int)
    add.add_argument("--retries", type=nonnegative_int)
    add.add_argument("--elapsed-seconds", type=nonnegative_decimal)
    add.add_argument("--cost-amount", type=nonnegative_decimal)
    add.add_argument("--currency", help="three-letter currency code, e.g. USD or CNY")
    add.add_argument("--pattern", action="append", choices=PATTERNS, default=[],
                     help="suspected workflow pattern; this is a hypothesis, not a finding")
    add.add_argument("--evidence", action="append", required=True,
                     help="durable result/verification reference; repeat as needed")
    add.set_defaults(handler=record)

    inspect = subparsers.add_parser("review", help="summarize recorded samples by task class and route")
    inspect.add_argument("--home", default="~/.ena")
    inspect.add_argument("--task-class", help="optional task-class filter")
    inspect.set_defaults(handler=review)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
