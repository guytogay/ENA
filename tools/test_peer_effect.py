#!/usr/bin/env python3
"""Regression for the A2A effect observation primitive (issue #88).

The property under test is narrow and easy to fake: a dispatched task's durable effect inside a
declared scope must be observable from outside the dispatched session, so that a child session's
narrative is never the evidence. Each test below fails for a specific wrong implementation —
including the pleasant one where the tool reports exactly what the caller hoped for.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TOOL = REPO / "tools" / "ena_peer_effect.py"


def run(*args: str, expect: int = 0) -> subprocess.CompletedProcess:
    """Run the tool and demand the exit code.

    The exit code is read from the process, never through a pipeline, because reading it through one
    is how a failing check gets reported as a passing one.
    """
    proc = subprocess.run([sys.executable, str(TOOL), *args], capture_output=True, text=True,
                          encoding="utf-8", errors="replace")
    if proc.returncode != expect:
        raise AssertionError(f"exit {proc.returncode} != {expect} for {args}\n"
                             f"stdout={proc.stdout}\nstderr={proc.stderr}")
    return proc


def receipt(proc: subprocess.CompletedProcess) -> dict:
    line = [row for row in proc.stdout.strip().splitlines() if row.startswith("{")]
    if len(line) != 1:
        raise AssertionError(f"expected exactly one receipt line on stdout, got {proc.stdout!r}")
    return json.loads(line[0])


class PeerEffectObservationTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.scope = self.root / "scope"
        self.scope.mkdir()
        self.before = self.root / "before.json"
        self.record = self.root / "record.json"
        self.index = self.root / "index.jsonl"

    def tearDown(self):
        self._tmp.cleanup()

    def snapshot(self):
        run("snapshot", "--scope", str(self.scope), "--out", str(self.before))

    def record_after(self, correlation="corr-1", index=None, expect=0):
        args = ["record", "--before", str(self.before), "--correlation-id", correlation,
                "--out", str(self.record)]
        if index:
            args += ["--index", str(index)]
        return run(*args, expect=expect)

    def load_record(self) -> dict:
        return json.loads(self.record.read_text(encoding="utf-8"))

    # 1
    def test_creation_is_reported_as_added(self):
        self.snapshot()
        (self.scope / "created.txt").write_text("new\n", encoding="utf-8")
        self.assertEqual(receipt(self.record_after())["added_count"], 1)
        self.assertIn("created.txt", self.load_record()["effects"]["added"])

    # 2
    def test_deletion_is_reported_as_removed(self):
        (self.scope / "doomed.txt").write_text("here\n", encoding="utf-8")
        self.snapshot()
        (self.scope / "doomed.txt").unlink()
        self.assertEqual(receipt(self.record_after())["removed_count"], 1)
        self.assertIn("doomed.txt", self.load_record()["effects"]["removed"])

    # 3
    def test_content_change_is_reported_as_modified(self):
        target = self.scope / "changed.txt"
        target.write_text("before\n", encoding="utf-8")
        self.snapshot()
        target.write_text("after\n", encoding="utf-8")
        self.assertEqual(receipt(self.record_after())["modified_count"], 1)
        self.assertIn("changed.txt", self.load_record()["effects"]["modified"])

    def test_rewriting_the_same_content_is_not_a_change(self):
        """A content digest, not a timestamp, decides `modified`."""
        target = self.scope / "same.txt"
        target.write_text("identical\n", encoding="utf-8")
        self.snapshot()
        target.write_text("identical\n", encoding="utf-8")     # same bytes, new mtime
        self.assertEqual(receipt(self.record_after())["modified_count"], 0)

    # 4
    def test_an_unchanged_tree_reports_zero_effect(self):
        (self.scope / "quiet.txt").write_text("nothing happens\n", encoding="utf-8")
        self.snapshot()
        got = receipt(self.record_after())
        self.assertEqual([got["added_count"], got["removed_count"], got["modified_count"]], [0, 0, 0])

    # 5
    def test_a_child_narrative_is_not_evidence(self):
        """The tool never reads a child's report: a confident 'DONE' leaves the effect at zero, and
        real changes are recorded with no narrative at all."""
        self.snapshot()
        (self.root / "child-said.txt").write_text("DONE - all files created\n", encoding="utf-8")
        self.assertEqual(receipt(self.record_after())["added_count"], 0)
        (self.scope / "actually-created.txt").write_text("x\n", encoding="utf-8")
        self.assertEqual(receipt(self.record_after())["added_count"], 1)

    # 6
    def test_the_correlation_id_reaches_both_the_record_and_the_receipt(self):
        self.snapshot()
        got = receipt(self.record_after(correlation="task-abc-123"))
        self.assertEqual(got["correlation_id"], "task-abc-123")
        self.assertEqual(self.load_record()["correlation_id"], "task-abc-123")

    # 7
    def test_the_index_keeps_earlier_entries(self):
        (self.scope / "a.txt").write_text("a\n", encoding="utf-8")
        self.snapshot()
        self.record_after(correlation="first", index=str(self.index))
        (self.scope / "b.txt").write_text("b\n", encoding="utf-8")
        self.record_after(correlation="second", index=str(self.index))
        rows = [json.loads(line) for line in self.index.read_text(encoding="utf-8").splitlines()]
        self.assertEqual([row["correlation_id"] for row in rows], ["first", "second"])
        self.assertTrue(all(Path(row["record"]).is_file() for row in rows))

    # 8
    def test_a_symlink_cannot_expand_the_observed_scope(self):
        outside = self.root / "outside"
        outside.mkdir()
        (outside / "untracked.txt").write_text("before\n", encoding="utf-8")
        try:
            (self.scope / "link").symlink_to(outside, target_is_directory=True)
        except (OSError, NotImplementedError) as exc:
            # Creating a symlink needs a privilege Windows does not grant by default. The check did
            # not run here, so it is reported as not run -- never as passing.
            self.skipTest(f"this platform cannot create a symlink: {exc}")
        self.snapshot()
        (outside / "untracked.txt").write_text("after\n", encoding="utf-8")
        (outside / "brand-new.txt").write_text("new\n", encoding="utf-8")
        got = receipt(self.record_after())
        self.assertEqual([got["added_count"], got["modified_count"]], [0, 0])
        entry = self.load_record()["after"]["link"]
        self.assertEqual(entry["kind"], "symlink")

    # 9
    def test_a_missing_declared_scope_fails_visibly(self):
        missing = self.root / "never-existed"
        proc = run("snapshot", "--scope", str(missing), "--out", str(self.before), expect=3)
        self.assertIn("declared scope missing", proc.stderr)
        payload = json.loads(self.before.read_text(encoding="utf-8"))
        self.assertFalse(payload["complete"])
        self.assertEqual(payload["entries"], {})

    def test_a_record_over_a_disappeared_scope_is_incomplete_not_empty(self):
        (self.scope / "x.txt").write_text("x\n", encoding="utf-8")
        self.snapshot()
        for child in self.scope.iterdir():
            child.unlink()
        self.scope.rmdir()
        proc = self.record_after(expect=3)
        self.assertEqual(receipt(proc)["removed_count"], 1)
        record = self.load_record()
        self.assertFalse(record["complete"])
        self.assertTrue(any("declared scope missing" in item for item in record["limitations"]))

    def test_the_boundary_is_stated_in_the_record(self):
        self.snapshot()
        self.record_after()
        record = self.load_record()
        self.assertIn("observation boundary", record["observation_boundary"])
        self.assertEqual(record["scopes"], [str(self.scope.resolve())])

    # 10
    def test_actor_attribution_behaviour_is_unchanged(self):
        """The effect receipt does not replace actor attribution: peer identity still comes from
        ENA_PEER_CALLER / ENA_PEER_TASK_ID through the existing helper."""
        env = dict(os.environ, ENA_PEER_CALLER="pc-dsh", ENA_PEER_TASK_ID="task-test-123")
        proc = subprocess.run([sys.executable, str(REPO / "tools" / "ena_actor.py")],
                              capture_output=True, text=True, encoding="utf-8", env=env)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        actor = json.loads(proc.stdout)
        self.assertEqual(actor["initiated_by"], "peer:pc-dsh")
        self.assertEqual(actor["channel"], "a2a")
        self.assertEqual(actor["correlation_id"], "task-test-123")

    def test_the_tool_declares_itself_optional_and_scope_limited(self):
        """A reader must be able to see that this is not a gate and not a machine-wide claim."""
        doc = (REPO / "A2A.md").read_text(encoding="utf-8")
        self.assertIn("observation boundary, not an authorization boundary", doc)
        self.assertIn("ena_peer_effect.py", doc)
        self.assertIn("not a claim that the whole machine was unchanged elsewhere", doc)


if __name__ == "__main__":
    unittest.main(verbosity=2)
