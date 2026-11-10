#!/usr/bin/env python3
"""Tests for the opt-in, quality-first resource ledger."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"


def run_tool(*args: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-B", *map(str, args)],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )


class ResourceLedgerTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.home = self.tmp / "home"
        init = run_tool(
            TOOLS / "ena_init.py",
            "--home", self.home,
            "--timezone", "Etc/UTC",
            "--language", "en-US",
        )
        self.assertEqual(init.returncode, 0, init.stdout + init.stderr)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def record(
        self,
        task_id: str,
        *,
        task_class: str = "code-fix",
        route: str = "model-a",
        outcome: str = "complete",
        quality: str = "verified",
        input_tokens: int | None = 100,
        output_tokens: int | None = 50,
        extra: tuple[str, ...] = (),
    ) -> Path:
        args: list[object] = [
            TOOLS / "resource_ledger.py", "record",
            "--home", self.home,
            "--task-id", task_id,
            "--task-class", task_class,
            "--route", route,
            "--outcome", outcome,
            "--quality", quality,
            "--usage-source", "provider",
            "--evidence", f"test:{task_id}",
        ]
        if input_tokens is not None:
            args.extend(["--input-tokens", str(input_tokens)])
        if output_tokens is not None:
            args.extend(["--output-tokens", str(output_tokens)])
        args.extend(extra)
        result = run_tool(*args)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        target = Path(result.stdout.strip())
        self.assertTrue(target.is_file())
        return target

    def test_record_is_metadata_only_and_preserves_provenance(self) -> None:
        target = self.record(
            "task-1",
            extra=(
                "--tool-calls", "4",
                "--retries", "1",
                "--elapsed-seconds", "12.5",
                "--cost-amount", "0.0042",
                "--currency", "USD",
                "--pattern", "blind-retry",
            ),
        )
        record = json.loads(target.read_text(encoding="utf-8"))
        self.assertEqual(record["schema_version"], "0.1")
        self.assertEqual(record["task"]["class"], "code-fix")
        self.assertEqual(record["task"]["route"], "model-a")
        self.assertEqual(record["task"]["outcome"], "complete")
        self.assertEqual(record["task"]["quality"], "verified")
        self.assertEqual(record["usage_source"], "provider")
        self.assertEqual(record["usage"]["input_tokens"], 100)
        self.assertEqual(record["usage"]["output_tokens"], 50)
        self.assertEqual(record["usage"]["tool_calls"], 4)
        self.assertEqual(record["usage"]["retries"], 1)
        self.assertEqual(record["usage"]["elapsed_seconds"], "12.5")
        self.assertEqual(record["usage"]["provider_cost"], "0.0042")
        self.assertEqual(record["usage"]["currency"], "USD")
        self.assertEqual(record["suspected_patterns"], ["blind-retry"])
        self.assertEqual(record["evidence_refs"], ["test:task-1"])
        self.assertNotIn("prompt", record)
        self.assertNotIn("trace", record)

    def test_review_compares_outcomes_and_reports_sample_sizes(self) -> None:
        self.record("task-1", extra=("--pattern", "blind-retry"))
        self.record("task-2", input_tokens=200, output_tokens=100)
        self.record(
            "task-3",
            outcome="failed",
            quality="not_verified",
            input_tokens=300,
            output_tokens=100,
        )
        self.record(
            "task-4",
            task_class="research",
            route="model-b",
            input_tokens=900,
            output_tokens=300,
        )

        result = run_tool(
            TOOLS / "resource_ledger.py", "review",
            "--home", self.home,
            "--task-class", "code-fix",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["records_reviewed"], 3)
        self.assertEqual(len(report["groups"]), 1)
        group = report["groups"][0]
        self.assertEqual(group["task_class"], "code-fix")
        self.assertEqual(group["route"], "model-a")
        self.assertEqual(group["outcomes"]["complete"], 2)
        self.assertEqual(group["outcomes"]["failed"], 1)
        self.assertEqual(group["verified_completions"], 2)
        self.assertEqual(group["verified_completion_usage_samples"], 2)
        self.assertEqual(group["median_tokens_per_verified_completion"], 225)
        self.assertEqual(group["other_outcome_usage_samples"], 1)
        self.assertEqual(group["median_tokens_per_other_outcome"], 400)
        self.assertEqual(group["pattern_hypotheses"], {"blind-retry": 1})
        self.assertIn("There is no per-Agent ranking", report["interpretation_limits"][6])

    def test_unknown_usage_is_not_invented(self) -> None:
        target = self.record("task-unknown", input_tokens=None, output_tokens=None)
        record = json.loads(target.read_text(encoding="utf-8"))
        self.assertEqual(record["usage"]["input_tokens"], None)
        self.assertEqual(record["usage"]["output_tokens"], None)

        result = run_tool(TOOLS / "resource_ledger.py", "review", "--home", self.home)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        group = json.loads(result.stdout)["groups"][0]
        self.assertEqual(group["verified_completions"], 1)
        self.assertEqual(group["verified_completion_usage_samples"], 0)
        self.assertIsNone(group["median_tokens_per_verified_completion"])

    def test_missing_evidence_is_rejected(self) -> None:
        result = run_tool(
            TOOLS / "resource_ledger.py", "record",
            "--home", self.home,
            "--task-id", "task-1",
            "--task-class", "code-fix",
            "--outcome", "complete",
        )
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("Traceback", result.stderr)

    def test_negative_usage_is_rejected(self) -> None:
        result = run_tool(
            TOOLS / "resource_ledger.py", "record",
            "--home", self.home,
            "--task-id", "task-1",
            "--task-class", "code-fix",
            "--outcome", "complete",
            "--evidence", "test:negative",
            "--input-tokens", "-1",
        )
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("Traceback", result.stderr)

    def test_cost_and_currency_must_be_supplied_together(self) -> None:
        result = run_tool(
            TOOLS / "resource_ledger.py", "record",
            "--home", self.home,
            "--task-id", "task-1",
            "--task-class", "code-fix",
            "--outcome", "complete",
            "--evidence", "test:cost",
            "--cost-amount", "0.01",
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("--currency is required", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_task_class_is_a_bounded_label(self) -> None:
        result = run_tool(
            TOOLS / "resource_ledger.py", "record",
            "--home", self.home,
            "--task-id", "task-1",
            "--task-class", "../private",
            "--outcome", "complete",
            "--evidence", "test:label",
        )
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("Traceback", result.stderr)

    def test_recorded_paths_remain_inside_home(self) -> None:
        config = self.home / "ENA.yaml"
        text = config.read_text(encoding="utf-8").replace(
            "records: evolution", "records: ../outside"
        )
        config.write_text(text, encoding="utf-8")
        result = run_tool(
            TOOLS / "resource_ledger.py", "record",
            "--home", self.home,
            "--task-id", "task-1",
            "--task-class", "code-fix",
            "--outcome", "complete",
            "--evidence", "test:path",
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("outside the active ENA home", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
