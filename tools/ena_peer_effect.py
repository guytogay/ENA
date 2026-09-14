#!/usr/bin/env python3
"""Observe the durable effect of dispatched work over a declared scope.

A bridge or runtime records the request it forwarded and whatever the child session narrated back.
Neither says what the work created, changed or removed. This helper supplies exactly that missing
half: it snapshots the declared scope before dispatch, re-observes the same scope after the
dispatched process exits, and writes a durable record of the difference (issue #88).

It is a **reference observation primitive**, not a wire protocol and not a control-file schema:

* the declared scope is an **observation boundary, not an authorization boundary** -- authorization
  belongs to the Host, and this tool never refuses work because an effect was unexpected;
* a record proves what was observed **inside the declared scopes only**; it is not a claim that the
  rest of the machine was unchanged;
* to call the result Host-generated evidence, run the observation and store the record outside the
  dispatched session's writable surface. The tool cannot check that for you, so the record says which
  scopes it observed and nothing more.

Usage:

    python tools/ena_peer_effect.py snapshot --scope <path> [--scope <path> ...] --out before.json
    python tools/ena_peer_effect.py record --before before.json --correlation-id <id> \\
        --out record.json [--index index.jsonl]

`record` prints one JSON receipt line on stdout:

    {"correlation_id": ..., "record": ..., "added_count": ..., "removed_count": ..., "modified_count": ...}

Exit codes:

    0  observed completely
    2  usage or input error (unreadable control input, no scope declared)
    3  observed with limitations (a declared scope is missing or unreadable) -- the record is still
       written and marks itself incomplete, because a false empty record is worse than a partial one
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

RECORD_SCHEMA = "ena-peer-effect-record/1"
SNAPSHOT_SCHEMA = "ena-peer-effect-snapshot/1"
READ_CHUNK = 1024 * 1024


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(READ_CHUNK), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def observe_scope(scope: Path) -> tuple[dict[str, dict], list[str]]:
    """Return {relative path -> entry} for one declared scope plus any observed limitations.

    Symlinks are recorded as symlinks and never followed, so a link cannot silently expand the
    observation surface beyond what was declared. Files are compared by content digest so a
    `modified` entry reflects observed content rather than a timestamp.
    """
    entries: dict[str, dict] = {}
    limitations: list[str] = []

    if not scope.exists():
        return entries, [f"declared scope missing: {scope}"]
    if not scope.is_dir():
        limitations.append(f"declared scope is not a directory: {scope}")
        return entries, limitations

    def walk(directory: Path, depth: int) -> None:
        if depth > 64:
            limitations.append(f"depth limit reached at {directory}")
            return
        try:
            children = sorted(directory.iterdir(), key=lambda item: item.name)
        except OSError as exc:
            limitations.append(f"unreadable directory {directory}: {exc.strerror or exc}")
            return
        for child in children:
            key = _relative(child, scope)
            try:
                info = child.lstat()
            except OSError as exc:
                limitations.append(f"unreadable path {child}: {exc.strerror or exc}")
                continue
            if child.is_symlink():
                try:
                    target = os.readlink(child)
                except OSError as exc:
                    limitations.append(f"unreadable symlink {child}: {exc.strerror or exc}")
                    target = None
                entries[key] = {"kind": "symlink", "target": target}
                continue
            if child.is_dir():
                entries[key] = {"kind": "dir"}
                walk(child, depth + 1)
                continue
            if not child.is_file():
                entries[key] = {"kind": "other", "size": info.st_size}
                continue
            try:
                entries[key] = {"kind": "file", "size": info.st_size, "sha256": _digest(child)}
            except OSError as exc:
                limitations.append(f"unreadable file {child}: {exc.strerror or exc}")
    walk(scope, 0)
    return entries, limitations


def observe(scopes: list[Path]) -> tuple[dict[str, dict], list[str], list[str]]:
    merged: dict[str, dict] = {}
    limitations: list[str] = []
    roots: list[str] = []
    for scope in scopes:
        resolved = scope.resolve()
        roots.append(str(resolved))
        entries, scope_limitations = observe_scope(resolved)
        limitations.extend(scope_limitations)
        for key, entry in entries.items():
            merged[f"{resolved}::{key}" if len(scopes) > 1 else key] = entry
    return merged, limitations, roots


def diff(before: dict[str, dict], after: dict[str, dict]) -> dict[str, list[str]]:
    added = sorted(key for key in after if key not in before)
    removed = sorted(key for key in before if key not in after)
    modified = sorted(key for key in before if key in after and before[key] != after[key])
    return {"added": added, "removed": removed, "modified": modified}


def command_snapshot(args: argparse.Namespace) -> int:
    scopes = [Path(value) for value in args.scope]
    entries, limitations, roots = observe(scopes)
    payload = {
        "snapshot_schema": SNAPSHOT_SCHEMA,
        "created_at": _iso_now(),
        "scopes": roots,
        "complete": not limitations,
        "limitations": limitations,
        "entries": entries,
    }
    Path(args.out).write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"snapshot: {args.out} ({len(entries)} entries, complete={payload['complete']})",
          file=sys.stderr)
    for limitation in limitations:
        print(f"limitation: {limitation}", file=sys.stderr)
    return 3 if limitations else 0


def command_record(args: argparse.Namespace) -> int:
    try:
        before = json.loads(Path(args.before).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"ena_peer_effect: cannot read --before {args.before}: {exc}", file=sys.stderr)
        return 2

    roots = before.get("scopes") or []
    if not roots:
        print("ena_peer_effect: the before-snapshot declares no scope", file=sys.stderr)
        return 2

    after_entries, limitations, _ = observe([Path(root) for root in roots])
    before_entries = before.get("entries", {})
    effects = diff(before_entries, after_entries)
    complete = bool(before.get("complete", True)) and not limitations

    record = {
        "record_schema": RECORD_SCHEMA,
        "correlation_id": args.correlation_id,
        "created_at": _iso_now(),
        "scopes": roots,
        "observation_boundary": ("observation boundary only: this record proves what was observed "
                                 "inside the declared scopes and is not a claim about paths "
                                 "outside them"),
        "complete": complete,
        "limitations": list(before.get("limitations", [])) + limitations,
        "effects": effects,
        "counts": {name: len(values) for name, values in effects.items()},
        "before": before_entries,
        "after": after_entries,
    }
    Path(args.out).write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if args.index:
        locator = {
            "created_at": record["created_at"],
            "correlation_id": args.correlation_id,
            "record": args.out,
            "scopes": roots,
            "complete": complete,
            **record["counts"],
        }
        with Path(args.index).open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(locator, ensure_ascii=False) + "\n")

    receipt = {
        "correlation_id": args.correlation_id,
        "record": args.out,
        "added_count": len(effects["added"]),
        "removed_count": len(effects["removed"]),
        "modified_count": len(effects["modified"]),
    }
    print(json.dumps(receipt, ensure_ascii=False))
    for limitation in record["limitations"]:
        print(f"limitation: {limitation}", file=sys.stderr)
    return 3 if not complete else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Observe what dispatched work changed inside a declared scope.")
    sub = parser.add_subparsers(dest="command", required=True)

    snap = sub.add_parser("snapshot", help="observe the declared scopes before dispatch")
    snap.add_argument("--scope", action="append", required=True,
                      help="declared observation scope (repeatable)")
    snap.add_argument("--out", required=True, help="where to write the before-snapshot")
    snap.set_defaults(func=command_snapshot)

    rec = sub.add_parser("record", help="observe again after the dispatched work exits")
    rec.add_argument("--before", required=True, help="the before-snapshot written by `snapshot`")
    rec.add_argument("--correlation-id", required=True,
                     help="the same task/correlation id used for attribution")
    rec.add_argument("--out", required=True, help="where to write the durable work record")
    rec.add_argument("--index", help="optional JSONL locator index to append to")
    rec.set_defaults(func=command_record)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
