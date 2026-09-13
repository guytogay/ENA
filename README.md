# ENA

Release: v2.0.0 — strengthened readiness provenance, SAFE-CHANGE recovery contracts, and evidence reproducibility. See `CHANGELOG.md` and `RELEASE-NOTES.md`.

ENA helps an Agent add runtime capabilities that reasoning alone does not provide: grounded self-inspection, external recovery, reversible self-change, cross-session memory maintenance, idea variation, and evidence-backed evolution.

ENA does not replace the model's ordinary judgment or add a second reasoning bureaucracy around it.

New adopters should use this repository. The older `evolution-native-agent-architecture` repository preserves the previous release line, research evidence, and project history; do not treat its `releases/current/` tree as the install path for this product.

## Start here

Read and apply these four in order:

1. `FIRST-USE.md` — establish the minimum real system map and shared settings. It carries the exact commands, the readiness predicate, trusted preset/unattended adoption, and what to do when no human is present.
2. `SURVIVAL.md` — keep a recovery path outside the current Agent failure surface.
3. `SAFE-CHANGE.md` — preserve the previous working state, prepare recovery, gate state transitions, and run the smallest relevant deterministic checks close to important changes. Session/coding Agents can start from `examples/change/SESSION-GIT-WORKTREE.md`.
4. `EVOLUTION.md` — preserve an improvement candidate, test it against reality, and keep/revise/reject/restore it while retaining useful validation/repair evidence.

**Read when a capability needs it, not as an adoption step:**

- `A2A.md` — when a two-way Agent-to-Agent path exists or is worth establishing. A2A is a collaboration and recovery capability, **not a universal installation gate**: if the Host cannot support it, record the limitation and continue.
- `SLEEP-DREAM-QUICKSTART.md` (with `SLEEP-DREAM.md` for the full mechanism) — the experimental Sleep/Dream cycle. Its marginal value over ordinary model reasoning is **unmeasured**, and its sampler parameters are experimental; run it when you want the experiment, not to complete adoption.
- `tools/README.md` — runnable examples, the reference-tool inventory, and the centralized READY/NOT_READY interaction table. `tools/EXIT-CODES.md` carries the exit-code contract.
- `UPGRADING.md` — **only** for an existing ENA home or SAFE-CHANGE package from an earlier release. Read it before treating a new refusal as an environment failure.

The first command of a cold or incremental First Use:

```bash
python tools/ena_first_use.py --home ~/.ena
```

With no confirmed timezone/language authority it exits `2` as `NOT_READY` and does not manufacture an initialized home. `FIRST-USE.md` carries the rest: the confirmed-value flags, the evidence-bearing `--verified-*` updates, and the conditions under which the home becomes READY.

## Reading is not installation

For a capability you choose to adopt, completion requires one of these:

- a real Host/runtime mechanism was configured and verified; or
- `SYSTEM.yaml` explicitly records that the capability is `UNAVAILABLE` or `NOT_NEEDED` on this Host, with enough reason to avoid silently forgetting the gap.

Acknowledging, summarizing or agreeing with a document does not install the capability.

Reference scripts only enforce what the Host actually routes through them. For example, `ena_preflight.py` is a real non-zero gate only when session/startup wiring honors its exit status, and `safe_change_state.py` prevents invalid SAFE-CHANGE transitions only when state changes go through it or an equivalent Host-native boundary. ENA cannot intercept arbitrary manual edits without Host cooperation.

`ena_preflight.py` decides whether the home is ready for ordinary ENA-active work. A successful setup/repair/reference-tool action does not imply that First Use is complete. Some tools intentionally remain usable while the home is `NOT_READY` so they can help establish or repair the missing capability.

## Make First Use happen without a reminder

If the Host supports a session-start, shell-start, Agent-start or workspace-start hook, run

```bash
python tools/ena_preflight.py --home ~/.ena
```

before ordinary work; if it has no startup hook, run the same preflight at the start of a new working session. A non-zero exit means the local setup is missing, the strengthened minimum readiness predicate does not pass, or `SYSTEM.yaml` is stale — run `ena_first_use.py` / refresh First Use instead of merely acknowledging the instruction and continuing. `FIRST-USE.md` states the predicate, the freshness window, and how a trusted deployment policy may pre-provision the values so First Use can run unattended.

## Local files

A typical installation starts with `ENA.yaml`, `SYSTEM.yaml`, `changes/` and `evolution/` under `~/.ena/`; `FIRST-USE.md` gives the minimum shape of both control files. Two rules matter before writing either:

- `ENA.example.yaml` and `examples/SYSTEM.example.yaml` are templates, not live-state replacement commands. Replace confirmed placeholders before use, and never overwrite an established `SYSTEM.yaml` with the shipped example: doing so would discard freshness-bounded operational facts and verification evidence outside the reference tools' control.
- Control files use a strict mapping/scalar YAML subset. Block sequences (`- item`) and multiline/block scalars are not accepted by `tools/control_yaml.py`; documented machine-read examples must stay inside that subset.

## Reference tools

`tools/` holds small standard-library Python examples and the shared helper modules they use. `tools/README.md` is the inventory and the runnable-example surface; prefer stronger Host-native backup, scheduler, snapshot, validation hook, A2A, or memory mechanisms when they already exist.

## License

Licensed under the Apache License, Version 2.0. See `LICENSE`.
