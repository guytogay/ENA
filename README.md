# ENA

ENA helps an Agent build practical infrastructure for survivability, collaboration, protected self-change, and evolution around the Host it actually has.

This repository is under active development and is **not yet the Current release**.

## Use order

1. [`FIRST-USE.md`](FIRST-USE.md) — inspect the real Agent/Host, confirm shared timezone/language/home, and write `ENA.yaml` plus `BODY.yaml`.
2. [`A2A.md`](A2A.md) — reuse or establish a real bidirectional A2A path, Agent Card, and at least one usable rescue peer.
3. [`SURVIVAL.md`](SURVIVAL.md) — build an external restart/recovery ladder that remains available when the main Agent is unhealthy.
4. [`ACMS.md`](ACMS.md) — route critical body changes through preserved known-good state, executable rollback, timed automatic recovery, and an externally shared rescue package.
5. [`EVOLUTION.md`](EVOLUTION.md) — turn improvement candidates into bounded trials, compare them with real baseline evidence, and retain/revise/reject/restore the result.

[`ENA.example.yaml`](ENA.example.yaml) shows the shared local configuration shape. Examples under [`examples/`](examples/) show body, ACMS rescue/status, and evolution candidate records.

## Current build shape

```text
First Use: inspect + normalize
        ↓
A2A: establish external collaboration/rescue reach
        ↓
Survival: external restart + recovery ladder
        ↓
ACMS: protected body-change path
        ↓
Evolution: cumulative observed improvement
```

The Host may already provide better native mechanisms for some of these capabilities. Reuse those mechanisms and record the actual integration rather than rebuilding equivalent infrastructure only for ENA.

## Current release

The existing Current release remains `v0.3.14 / FIELD_VALIDATION` in `guytogay/evolution-native-agent-architecture`.
