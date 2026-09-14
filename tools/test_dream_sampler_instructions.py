#!/usr/bin/env python3
"""Regression teeth for the Dream sampler's own operating instructions (ENA #93).

The ruling on #93 was: do not change the sampler, document what its two controls actually do. A
clarification that only lives in prose rots the moment someone edits the prose, so this asserts the
statements that were measured — plus the behaviour behind them, so the help cannot drift away from
what the tool does.

Teeth are stated as: if a later edit re-introduces a bare `--seed 42` in the documented example, or
strips the count/anchor explanation, or changes the default count, this file goes red.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TOOL = REPO / "tools" / "dream_sample.py"
README = REPO / "tools" / "README.md"


class DreamSamplerInstructionTests(unittest.TestCase):
    """Assertions match on collapsed whitespace.

    argparse wraps help text to the terminal width, so a phrase can straddle a line break. Matching
    the raw output would make this file fail on reformatting rather than on a lost instruction - the
    instrument failing instead of the subject.
    """

    @staticmethod
    def _flatten(text: str) -> str:
        return " ".join(text.split())

    @classmethod
    def setUpClass(cls):
        proc = subprocess.run([sys.executable, "-B", str(TOOL), "--help"], capture_output=True,
                              text=True, encoding="utf-8", errors="replace")
        cls.help_text = cls._flatten(f"{proc.stdout}{proc.stderr}")
        cls.readme = cls._flatten(README.read_text(encoding="utf-8"))

    def test_help_says_count_includes_the_anchor_and_names_the_omitted_pool_consequence(self):
        lowered = self.help_text.lower()
        self.assertIn("including the anchor", lowered,
                      "--count help no longer says the anchor consumes one of its slots")
        self.assertIn("one pool is omitted", lowered,
                      "--count help no longer states that a pool is omitted at the default")
        self.assertIn("not a coverage guarantee", lowered,
                      "--count help no longer disclaims --count 7 as a coverage guarantee")

    def test_help_says_a_seed_is_for_replay_and_should_be_omitted_for_live_runs(self):
        lowered = self.help_text.lower()
        self.assertIn("replay/debugging control", lowered,
                      "--seed help no longer says what the control is for")
        self.assertIn("omit it for recurring", lowered,
                      "--seed help no longer tells a scheduled run to omit the seed")
        self.assertIn("pins which pool is omitted", lowered,
                      "--seed help no longer states the measured side effect of a fixed seed")

    def test_the_default_count_is_still_six(self):
        """The ruling kept the default; a silent change would invalidate the documentation."""
        match = re.search(r"--count\s+COUNT", self.help_text)
        self.assertIsNotNone(match, "--count disappeared from the CLI")
        self.assertIn("default: 6", self.help_text,
                      "the default fragment count changed; the documented explanation is now stale")

    def test_the_documented_example_does_not_pin_a_seed(self):
        """A copied example is how a fixed seed gets into a scheduled run."""
        block = self.readme.split("python tools/dream_sample.py", 1)[1].split("```", 1)[0]
        self.assertNotIn("--seed", block,
                         "the documented example pins --seed again; recurring runs should omit it")
        self.assertIn("--count", self.readme.lower().replace("--count", "--count") or "",
                      "the count/anchor explanation vanished from tools/README.md")

    def test_readme_keeps_the_three_measured_facts(self):
        for phrase in ("replay/debugging control", "includes the anchor",
                       "pins the position drawn inside a pool"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.lower(), self.readme.lower(),
                              f"tools/README.md no longer states: {phrase}")

    def test_omitting_the_seed_still_generates_and_records_one(self):
        """The behaviour the documentation tells a scheduled run to rely on."""
        with tempfile.TemporaryDirectory() as tmp:
            material = Path(tmp) / "material.jsonl"
            material.write_text("".join(json.dumps({
                "id": f"mem-{i:03d}", "timestamp": f"2026-09-{i + 1:02d}T08:00:00+08:00",
                "salience": 1, "retrieval_count": 0, "source_type": "agent", "text": f"r{i}",
            }) + "\n" for i in range(12)), encoding="utf-8")
            out = Path(tmp) / "set.json"
            proc = subprocess.run([sys.executable, "-B", str(TOOL), "--memory", str(material),
                                   "--output", str(out)], capture_output=True, text=True,
                                  encoding="utf-8", errors="replace")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            data = json.loads(out.read_text(encoding="utf-8"))
            self.assertIsInstance(data["seed"], int,
                                  "the sampler no longer records the seed it generated")


if __name__ == "__main__":
    unittest.main(verbosity=2)
