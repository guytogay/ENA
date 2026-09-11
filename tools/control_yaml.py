#!/usr/bin/env python3
"""Strict reader for ENA-owned control YAML.

This is intentionally not a general YAML parser. It accepts only the small
mapping subset emitted by ENA reference tools: root scalars and one level of
nested scalar mappings. Unsupported YAML fails closed instead of being
silently misread.
"""

from __future__ import annotations

import re
from typing import Any


class ControlYamlError(ValueError):
    pass


_KEY = re.compile(r"^[A-Za-z0-9_.-]+$")


def _clean_scalar(raw: str) -> str:
    value = raw.strip()
    if value.startswith(("|", ">")):
        raise ControlYamlError("multiline/block scalars are not supported in ENA control YAML")
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def parse_control_yaml(text: str) -> dict[str, Any]:
    result: dict[str, Any] = {}
    current_section: str | None = None

    for lineno, raw in enumerate(text.splitlines(), start=1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if "\t" in raw[: len(raw) - len(raw.lstrip(" \t"))]:
            raise ControlYamlError(f"line {lineno}: tabs are not allowed for indentation")

        indent = len(raw) - len(raw.lstrip(" "))
        if indent not in {0, 2}:
            raise ControlYamlError(f"line {lineno}: only 0 or 2-space indentation is supported")

        line = raw[indent:]
        if line.startswith("- ") or line == "-":
            raise ControlYamlError(f"line {lineno}: sequence syntax is not supported")
        if ":" not in line:
            raise ControlYamlError(f"line {lineno}: expected key: value")

        key, raw_value = line.split(":", 1)
        key = key.strip()
        if not _KEY.fullmatch(key):
            raise ControlYamlError(f"line {lineno}: unsupported key {key!r}")
        value = _clean_scalar(raw_value)

        if indent == 0:
            current_section = None
            if key in result:
                raise ControlYamlError(f"line {lineno}: duplicate root key {key!r}")
            if value == "":
                result[key] = {}
                current_section = key
            else:
                result[key] = value
            continue

        if current_section is None:
            raise ControlYamlError(f"line {lineno}: nested key without a root section")
        section = result[current_section]
        if not isinstance(section, dict):
            raise ControlYamlError(f"line {lineno}: parent {current_section!r} is not a mapping")
        if key in section:
            raise ControlYamlError(f"line {lineno}: duplicate key {current_section}.{key}")
        if value == "":
            raise ControlYamlError(f"line {lineno}: nesting deeper than one level is not supported")
        section[key] = value

    return result


def scalar(data: dict[str, Any], key: str, *, section: str | None = None) -> str | None:
    value: Any
    if section is None:
        value = data.get(key)
    else:
        parent = data.get(section)
        if not isinstance(parent, dict):
            return None
        value = parent.get(key)
    return value if isinstance(value, str) else None


def missing(value: str | None) -> bool:
    return value is None or value.strip().lower() in {"", "unknown", "null", "none", "~", "[]"}
