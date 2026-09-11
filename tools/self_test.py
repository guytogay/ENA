#!/usr/bin/env python3
"""Run a local smoke test of the ENA reference tools without touching live Agent state."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


def raw(*args):
    return subprocess.run([sys.executable, *map(str, args)], text=True, capture_output=True)


def run(*args):
    result = raw(*args)
    if result.returncode:
        raise SystemExit(result.stdout + result.stderr)
    return result.stdout.strip()


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    tools = repo / "tools"
    examples = repo / "examples" / "evolution"

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)

        home = tmp / "ena-home"
        run(tools / "ena_init.py", "--home", home, "--timezone", "Etc/UTC", "--language", "en-US")
        assert (home / "ENA.yaml").is_file()
        system = home / "SYSTEM.yaml"
        assert system.is_file()

        preflight = raw(tools / "ena_preflight.py", "--home", home)
        assert preflight.returncode == 2
        assert "REFRESH REQUIRED" in preflight.stdout

        text = system.read_text(encoding="utf-8")
        text = text.replace("minimum_ready: false", "minimum_ready: true")
        text = text.replace("  primary: UNKNOWN\n  backup_or_snapshot", "  primary: git-revert\n  backup_or_snapshot", 1)
        text = text.replace("rescue:\n  primary: UNKNOWN\n  type: UNKNOWN", "rescue:\n  primary: human-operator\n  type: human")
        system.write_text(text, encoding="utf-8")
        run(tools / "ena_preflight.py", "--home", home)

        preset_home = tmp / "ena-preset"
        run(
            tools / "ena_init.py",
            "--home", preset_home,
            "--timezone", "Etc/UTC",
            "--language", "en-US",
            "--host-profile", "session",
            "--recovery", "git-revert",
            "--rescuer", "human-operator",
            "--rescuer-type", "human",
            "--verified-minimum",
        )
        run(tools / "ena_preflight.py", "--home", preset_home)

        package = Path(run(
            tools / "change_scaffold.py",
            "--home", preset_home,
            "--timezone", "Etc/UTC",
            "--profile", "session",
            "--name", "self-test",
        ))
        assert package.is_dir()
        assert (package / "rollback.py").is_file()

        blocked_arm = raw(tools / "safe_change_state.py", package, "armed")
        assert blocked_arm.returncode == 2

        rescue = package / "rescue.yaml"
        rescue_text = rescue.read_text(encoding="utf-8")
        replacements = {
            "target: UNKNOWN": "target: test-repository",
            "recovery_actor: UNKNOWN": "recovery_actor: human-operator",
            "where_to_act: UNKNOWN": "where_to_act: test-workspace",
            "changed: UNKNOWN": "changed: config-file",
            "known_good: UNKNOWN": "known_good: git-base-commit",
            "rollback_action: UNKNOWN": "rollback_action: git-revert-change",
            "restart_or_new_session: UNKNOWN": "restart_or_new_session: new-session",
            "verify_operation: UNKNOWN": "verify_operation: reference-self-test",
        }
        for old, new in replacements.items():
            rescue_text = rescue_text.replace(old, new)
        rescue.write_text(rescue_text, encoding="utf-8")

        run(tools / "safe_change_state.py", package, "armed")
        run(tools / "safe_change_state.py", package, "applied")
        no_evidence = raw(tools / "safe_change_state.py", package, "retained")
        assert no_evidence.returncode == 2
        run(tools / "safe_change_state.py", package, "retained", "--evidence", "self-test-pass")
        assert "state: retained" in (package / "status.yaml").read_text(encoding="utf-8")
        assert (package / "transitions.jsonl").is_file()

        validation = raw(
            tools / "validate_change.py",
            "--home", preset_home,
            "--name", "preflight-check",
            "--target", "SYSTEM.yaml",
            "--", sys.executable, tools / "ena_preflight.py", "--home", preset_home,
        )
        assert validation.returncode == 0
        validation_log = preset_home / "evolution" / "experience" / "validation-events.jsonl"
        events = [json.loads(line) for line in validation_log.read_text(encoding="utf-8").splitlines() if line.strip()]
        assert events[-1]["status"] == "pass"

        freshness_out = tmp / "freshness.json"
        run(
            tools / "freshness_scan.py",
            "--input", examples / "FRESHNESS.example.jsonl",
            "--output", freshness_out,
            "--now", "2026-09-12T03:00:00+08:00",
        )
        freshness = json.loads(freshness_out.read_text(encoding="utf-8"))
        assert freshness["counts"] == {"fresh": 1, "stale": 1, "unknown": 1}

        sleep_out = tmp / "sleep-input.json"
        run(
            tools / "sleep_prepare.py",
            "--experience", examples / "EXPERIENCE.example.jsonl",
            "--memory", examples / "MEMORY.example.jsonl",
            "--output", sleep_out,
        )
        assert json.loads(sleep_out.read_text(encoding="utf-8"))["task"] == "sleep_consolidation"

        dream_material = tmp / "dream-material.jsonl"
        run(
            tools / "combine_dream_material.py",
            "--memory", examples / "MEMORY.example.jsonl",
            "--knowledge", examples / "KNOWLEDGE.example.jsonl",
            "--capabilities", examples / "CAPABILITIES.example.jsonl",
            "--output", dream_material,
        )
        material_text = dream_material.read_text(encoding="utf-8")
        assert '"material_type": "knowledge"' in material_text
        assert '"material_type": "capability"' in material_text

        dream_out = tmp / "dream-set.json"
        run(
            tools / "dream_sample.py",
            "--memory", dream_material,
            "--output", dream_out,
            "--seed", "42",
        )
        dream = json.loads(dream_out.read_text(encoding="utf-8"))
        assert dream["truth_status"] == "speculative_input"
        assert dream["experimental_parameters"] is True
        assert dream["seed"] == 42
        assert dream["anchor_id"] is None
        assert dream["sampled_anchor_id"] is not None
        assert len(dream["input"]["sha256"]) == 64
        assert dream["input"]["record_count"] >= 2
        assert len(dream["fragments"]) >= 2

        replay_out = tmp / "dream-replay.json"
        run(
            tools / "dream_sample.py",
            "--memory", dream_material,
            "--output", replay_out,
            "--seed", str(dream["seed"]),
        )
        replay = json.loads(replay_out.read_text(encoding="utf-8"))
        assert replay == dream

        guided_out = tmp / "dream-guided.json"
        guided_anchor = dream["fragments"][0]["memory"]["id"]
        run(
            tools / "dream_sample.py",
            "--memory", dream_material,
            "--output", guided_out,
            "--mode", "problem-guided",
            "--anchor-id", guided_anchor,
            "--seed", "43",
        )
        guided = json.loads(guided_out.read_text(encoding="utf-8"))
        assert guided["anchor_id"] == guided_anchor
        assert guided["sampled_anchor_id"] is None

        auto_seed_out = tmp / "dream-auto-seed.json"
        run(
            tools / "dream_sample.py",
            "--memory", dream_material,
            "--output", auto_seed_out,
        )
        auto_seed = json.loads(auto_seed_out.read_text(encoding="utf-8"))["seed"]
        assert isinstance(auto_seed, int)

        candidate_path = Path(run(
            tools / "candidate_record.py",
            "--home", home,
            "--origin", "dream",
            "--candidate", "Try a different recovery sequence",
            "--reality-check", "Compare against one bounded real task",
        ))
        candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
        assert candidate["truth_status"] == "speculative"
        assert candidate_path.parent.name == "speculative"

    print("ENA reference tools: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
