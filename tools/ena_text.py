#!/usr/bin/env python3
"""Read ENA-owned text files as the Host actually writes them.

Control files and JSONL sources are usually created by a reference tool and then
edited by the Host operator. Some Host-native write paths prepend a UTF-8 byte
order mark: PowerShell 5.1 `Out-File -Encoding UTF8`, `Set-Content -Encoding
UTF8` and `Export-Csv` all do it by default on Windows.

A byte order mark carries no content, so accepting it cannot change what a
declared file means. Refusing it makes a control file that the Host wrote
correctly unreadable on that same Host, and turns an ordinary editing choice
into an opaque parsing failure. Every ENA-owned text read therefore goes through
this one function instead of restating an encoding decision per tool.
"""

from __future__ import annotations

from pathlib import Path


def read_text(path: Path) -> str:
    """Return the text of an ENA-owned file, tolerating a leading UTF-8 BOM."""
    return path.read_text(encoding="utf-8-sig")
