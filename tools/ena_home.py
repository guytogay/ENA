#!/usr/bin/env python3
"""One boundary for "is this an initialized ENA home, and which clock is it?".

Every reference tool that maintains durable ENA state has to answer the same two
questions before it writes anything. The tools used to answer them locally, and
the answers drifted:

- `validate_change.py` and `candidate_record.py` refused an uninitialized home,
  while `change_scaffold.py` created a package inside one and
  `safe_change_state.py` armed it;
- with no readable `ENA.yaml`, the state gate recorded `prepared -> armed` on a
  UTC clock while the package directory next to it was stamped with the caller's
  confirmed `+08:00` timezone.

Both are the same defect: a boundary that exists in the documentation but is not
enforced where the decision is made. This module is the single implementation of
that boundary, so a future fix cannot miss a sibling tool again.
"""

from __future__ import annotations

from pathlib import Path

from control_yaml import ControlYamlError, missing, parse_control_yaml, scalar
from ena_text import read_text
from timezone_utils import TimezoneUnavailable, load_timezone

INIT_HINT = "Run tools/ena_init.py first or pass --home to an initialized ENA home."
PACKAGE_LAYOUT_HINT = (
    "A SAFE-CHANGE package must live in <ENA home>/changes/<package> so the gate can read "
    "the owning ENA home; create it with tools/change_scaffold.py."
)


class EnaHomeError(ValueError):
    """Raised when an ENA home cannot supply the facts a maintaining tool requires."""


def read_control(path: Path) -> dict[str, object]:
    """Read one ENA control file, failing closed with an actionable error."""
    try:
        return parse_control_yaml(read_text(path))
    except (OSError, UnicodeError, ControlYamlError) as exc:
        raise EnaHomeError(f"{path.name} cannot be safely parsed: {exc}") from exc


def require_initialized_home(home: Path) -> tuple[object, str]:
    """Return `(tzinfo, canonical_name)` for an initialized home, or fail closed.

    `ENA.yaml` is the sole authority for the canonical timezone. Older schema-0.2
    homes may also carry a duplicate `SYSTEM.yaml canonical_timezone`; when that
    duplicate is known and disagrees, clock-dependent tools stop rather than
    silently choosing one side. If the legacy SYSTEM surface exists but cannot be
    parsed, the duplicate cannot be ruled out, so clock-dependent writes stop.
    """
    home = Path(home).expanduser().resolve()
    config = home / "ENA.yaml"
    if not config.is_file():
        raise EnaHomeError(f"ENA home is not initialized: missing {config}. {INIT_HINT}")

    data = read_control(config)
    name = scalar(data, "canonical_timezone")
    if missing(name):
        raise EnaHomeError(
            f"ENA home is not initialized: {config} has no canonical_timezone. {INIT_HINT}"
        )

    system = home / "SYSTEM.yaml"
    if system.is_file():
        system_data = read_control(system)
        system_name = scalar(system_data, "canonical_timezone")
        if not missing(system_name) and system_name != name:
            raise EnaHomeError(
                "canonical_timezone conflict: ENA.yaml is authoritative but SYSTEM.yaml "
                f"declares {system_name!r} while ENA.yaml declares {name!r}; reconcile the "
                "legacy duplicate before running a clock-dependent ENA tool"
            )

    try:
        return load_timezone(name), name
    except TimezoneUnavailable as exc:
        raise EnaHomeError(str(exc)) from exc


def home_of_package(package: Path) -> Path:
    """Return the ENA home that owns a SAFE-CHANGE package."""
    package = Path(package).expanduser().resolve()
    if package.parent.name != "changes":
        raise EnaHomeError(f"{package} is not a SAFE-CHANGE package. {PACKAGE_LAYOUT_HINT}")
    return package.parent.parent
