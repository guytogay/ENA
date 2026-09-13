#!/usr/bin/env python3
"""Adopter-facing documentation vs. the real CLI surface.

The commands and tool paths an adopter-facing document gives are part of ENA's interface: a renamed
flag or a tool that moved is only discovered by running the example and reading an argument error.
This regression keeps that surface honest, and it is deliberately structural and narrow:

* only lines that invoke ``tools/<tool>.py`` are read as commands, so a package-local or example
  name such as ``rollback.py`` in backticks is never reinterpreted as ``tools/rollback.py``, and a
  placeholder argument value such as ``--target tools/example.py`` is not read as a command;
* flags are validated against that tool's own ``--help`` output, so there is no second CLI schema
  in the test suite;
* no side-effectful example command is executed -- only ``--help``, and only for tools that parse
  arguments at all;
* the historical and release-operator surfaces (``CHANGELOG.md``, ``RELEASE-NOTES.md``,
  ``RELEASING.md``) are out of scope, because a past entry may legitimately name a tool that has
  since been renamed.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
TOOLS = REPO / "tools"
TOOLS_README = TOOLS / "README.md"

ADOPTER_DOCS = (
    REPO / "README.md",
    REPO / "FIRST-USE.md",
    REPO / "UPGRADING.md",
    REPO / "SAFE-CHANGE.md",
    REPO / "SURVIVAL.md",
    REPO / "A2A.md",
    REPO / "EVOLUTION.md",
    REPO / "SLEEP-DREAM.md",
    REPO / "SLEEP-DREAM-QUICKSTART.md",
    REPO / "examples/change/SESSION-GIT-WORKTREE.md",
    REPO / "tools/README.md",
    REPO / "tools/EXIT-CODES.md",
)

# A documented command example is a line that starts with a reference tool, optionally behind
# `python`/`python3` and `-B`; anything else is prose or a table row.
DOCUMENTED_COMMAND = re.compile(r"^(?:python3?\s+(?:-B\s+)?)?tools/([A-Za-z_]\w*\.py)\b(.*)$")
CONTINUATION = re.compile(r"\\\s*\n\s*")
FLAG = re.compile(r"(?<!\w)(--[a-z0-9][a-z0-9-]*)")

# The reference-tool inventory is the one fenced `text` block that lists tools one per line.
INVENTORY_BLOCK = re.compile(r"```text\n(.*?)```", re.DOTALL)
INVENTORY_ENTRY = re.compile(r"^([A-Za-z_]\w*\.py)\s", re.MULTILINE)

# A tool ships an entry point when it can be run as a script; test_*.py files are the CI suites,
# which are documented in the "Verify the tools" section instead of the inventory.
ENTRY_POINT = re.compile(r"^if\s+__name__\s*==\s*[\"']__main__[\"']\s*:", re.MULTILINE)

# Prose references are read from everything except the shell fences that hold command examples;
# those are the command scanner's property, not this one's.
SHELL_FENCE = re.compile(r"```(?:bash|sh|shell|console|python3?)\n.*?```", re.DOTALL)
TOOL_PATH = re.compile(r"tools/([A-Za-z_]\w*\.py)")


def documented_commands(text: str) -> list[tuple[str, str]]:
    """Every documented command that invokes a reference tool, as ``(tool, rest_of_command)``.

    Backslash continuations are joined first, so a multi-line example is checked as the operator
    would type it.
    """
    commands: list[tuple[str, str]] = []
    for line in CONTINUATION.sub(" ", text).splitlines():
        match = DOCUMENTED_COMMAND.match(line.strip())
        if match:
            commands.append((match.group(1), match.group(2)))
    return commands


class DocumentationSurfaceTests(unittest.TestCase):
    helps: dict[str, str] = {}

    @classmethod
    def cli_help(cls, tool: str) -> str:
        """The tool's real ``--help`` output, captured once per tool."""
        if tool not in cls.helps:
            environment = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
            result = subprocess.run(
                [sys.executable, "-B", str(TOOLS / tool), "--help"],
                cwd=str(REPO), env=environment, text=True, capture_output=True,
                encoding="utf-8", errors="replace",
            )
            cls.helps[tool] = f"{result.stdout}{result.stderr}"
        return cls.helps[tool]

    def test_the_documents_under_test_exist(self):
        # A rename must fail loudly here instead of quietly scanning nothing.
        missing = [str(path.relative_to(REPO)) for path in ADOPTER_DOCS if not path.is_file()]
        self.assertEqual(missing, [], f"adopter-facing documents are missing: {missing}")

    def test_documented_command_examples_are_runnable(self):
        seen = 0
        for path in ADOPTER_DOCS:
            for tool, rest in documented_commands(path.read_text(encoding="utf-8")):
                seen += 1
                with self.subTest(document=path.name, tool=tool):
                    tool_path = TOOLS / tool
                    self.assertTrue(
                        tool_path.is_file(),
                        f"{path.name} tells the reader to run tools/{tool}, which does not exist",
                    )
                    flags = sorted(set(FLAG.findall(rest)))
                    if not flags:
                        continue
                    source = tool_path.read_text(encoding="utf-8")
                    self.assertIn(
                        "argparse", source,
                        f"{path.name} passes {flags} to tools/{tool}, which parses no arguments",
                    )
                    help_text = self.cli_help(tool)
                    for flag in flags:
                        self.assertIn(
                            flag, help_text,
                            f"{path.name} documents {flag} for tools/{tool}, "
                            f"which its --help does not accept",
                        )
        self.assertGreater(seen, 0, "no documented tool command was found")

    def test_reference_tool_inventory_is_complete(self):
        text = TOOLS_README.read_text(encoding="utf-8")
        block = INVENTORY_BLOCK.search(text)
        self.assertIsNotNone(block, "tools/README.md no longer carries the reference-tool inventory")
        listed = set(INVENTORY_ENTRY.findall(block.group(1)))
        self.assertTrue(listed, "the reference-tool inventory lists no tool")

        shipped = {
            path.name for path in TOOLS.glob("*.py")
            if not path.name.startswith("test_")
            and ENTRY_POINT.search(path.read_text(encoding="utf-8"))
        }
        self.assertTrue(shipped, "no reference-tool entry point was detected")
        self.assertEqual(
            sorted(shipped - listed), [],
            "these reference tools ship an entry point but are missing from the inventory",
        )
        self.assertEqual(
            sorted(name for name in listed if not (TOOLS / name).is_file()), [],
            "the inventory names tools that do not exist",
        )

    def test_literal_tool_paths_in_adopter_prose_resolve(self):
        seen = 0
        for path in ADOPTER_DOCS:
            prose = SHELL_FENCE.sub("", path.read_text(encoding="utf-8"))
            for module in TOOL_PATH.findall(prose):
                seen += 1
                with self.subTest(document=path.name, module=module):
                    self.assertTrue(
                        (TOOLS / module).is_file(),
                        f"{path.name} refers to tools/{module}, which does not exist",
                    )
        self.assertGreater(seen, 0, "no literal tools/ path was found in adopter-facing prose")

    def test_the_scanner_does_not_read_non_tool_names_as_tool_paths(self):
        # Locked in deliberately: `rollback.py` is the package-local placeholder, and
        # `tools/example.py` is an illustrative --target value. Neither is a tool reference, and
        # neither may become a failure merely because it appears inside backticks.
        self.assertEqual(
            TOOL_PATH.findall(
                "The package-local `rollback.py` placeholder is created inside the change package, "
                "so the reader must not look for it beside the shipped tools."
            ),
            [],
        )
        self.assertEqual(documented_commands("  --target tools/example.py \\"), [])
        self.assertEqual(documented_commands("run `validate_change.py` and then `rollback.py`"), [])
        # ... while an explicit path is a reference and is checked.
        self.assertEqual(TOOL_PATH.findall("see tools/ena_init.py"), ["ena_init.py"])


if __name__ == "__main__":
    unittest.main()
