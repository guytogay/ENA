# ENA

ENA helps an Agent add runtime capabilities that reasoning alone does not provide: grounded self-inspection, external recovery, reversible self-change, cross-session memory maintenance, idea variation, and evidence-backed evolution.

ENA does not replace the model's ordinary judgment or add a second reasoning bureaucracy around it.

New adopters should use this repository. The older `evolution-native-agent-architecture` repository preserves the previous release line, research evidence, and project history; do not treat its `releases/current/` tree as the install path for this product.

## Start here

Read and apply these in order:

1. `FIRST-USE.md` — establish the minimum real system map and shared settings. It also explains trusted preset/unattended adoption.
2. `A2A.md` — reuse or establish a two-way Agent-to-Agent path when the Host can support it.
3. `SURVIVAL.md` — keep a recovery path outside the current Agent failure surface.
4. `SAFE-CHANGE.md` — preserve the previous working state and prepare recovery before an important self-change. Session/coding Agents can start from `examples/change/SESSION-GIT-WORKTREE.md`.
5. `EVOLUTION.md` — preserve an improvement candidate, test it against reality, and keep/revise/reject/restore it.
6. `SLEEP-DREAM-QUICKSTART.md` — run the first experimental Sleep and Dream cycle. `SLEEP-DREAM.md` contains the full mechanism.

## Reading is not installation

For a capability you choose to adopt, completion requires one of these:

- a real Host/runtime mechanism was configured and verified; or
- `SYSTEM.yaml` explicitly records that the capability is `UNAVAILABLE` or `NOT_NEEDED` on this Host, with enough reason to avoid silently forgetting the gap.

Acknowledging, summarizing or agreeing with a document does not install the capability.

## Make First Use happen without a reminder

If the Host supports a session-start, shell-start, Agent-start or workspace-start hook, run:

```bash
python tools/ena_preflight.py
```

before ordinary work.

The preflight fails when the local ENA setup is missing, First Use is not marked minimally ready, or `SYSTEM.yaml` is stale. In that case, refresh `FIRST-USE.md` first instead of merely acknowledging the instruction and continuing.

If the Host has no startup hook, run the same preflight at the start of a new working session.

A trusted deployment/workspace policy may pre-provision timezone, language, Host profile, recovery path and rescuer so First Use can run without interactive confirmation. See `FIRST-USE.md` and `tools/README.md`; missing policy values must remain unresolved rather than being replaced by guessed defaults.

## Local files

A typical installation starts with:

```text
~/.ena/
  ENA.yaml
  SYSTEM.yaml
  changes/
  evolution/
```

Use `ENA.example.yaml` and `examples/SYSTEM.example.yaml` as starting points.

## Reference tools

The `tools/` directory contains small standard-library Python examples:

```text
ena_init.py
ena_preflight.py
change_scaffold.py
sleep_prepare.py
dream_sample.py
candidate_record.py
self_test.py
```

Verify them with:

```bash
python tools/self_test.py
```

Then see `tools/README.md` for runnable examples. Prefer stronger Host-native backup, scheduler, snapshot, A2A or memory mechanisms when they already exist.
