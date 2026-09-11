# First Use

First Use should establish a usable minimum quickly. Unknown facts may remain `UNKNOWN`; do not turn first adoption into a full-system questionnaire.

Verify what can be inspected from the Host, runtime, files, tools, APIs or documentation. Do not guess when the environment can be checked.

## Minimum First Use

Complete these five things before treating ENA as active.

### 1. Confirm shared settings

Detect the Host/local timezone when possible, then ask the user to confirm the IANA timezone ENA should use. Do not impose a product default.

Use the current user interaction as a language hint when useful, then ask the user to confirm the working language tag such as `zh-CN` or `en-US`.

Ask where ENA-owned files should live. If the user has no preference, a stable user-home directory such as `~/.ena/` is suitable.

Keep commands, paths, identifiers, API fields and protocol payloads in the exact form required by their systems. Use UTF-8 for ENA-owned text unless an external interface requires otherwise.

### 2. Identify one real recovery path

Find at least one action that can recover useful operation without depending on the current Agent session remaining healthy.

Examples:

- restart through a service/process/container/VM supervisor;
- start a new coding/chat session against durable disk state;
- restore a Git revision/worktree/file backup/snapshot;
- another verified Host-native recovery action.

Record the exact mechanism, or `UNKNOWN` if none exists yet.

### 3. Identify one rescuer

A rescuer may be:

- a human who can access the Host/repository/recovery mechanism; or
- another Agent reachable through A2A and able to perform or relay recovery.

Human recovery is a valid first-class path. A2A is useful when supported, but it is not required merely to complete First Use.

### 4. Write `ENA.yaml` and `SYSTEM.yaml`

`ENA.yaml` keeps confirmed settings and stable pointers.

Minimum shape:

```yaml
ena_home: ~/.ena
canonical_timezone: REPLACE_WITH_CONFIRMED_IANA_TIMEZONE
canonical_language: REPLACE_WITH_CONFIRMED_LANGUAGE_TAG
text_encoding: UTF-8
```

`SYSTEM.yaml` is the current system map. At minimum record:

```yaml
checked_at: 2026-09-12T02:00:00+08:00
valid_until: 2026-09-19T02:00:00+08:00
minimum_ready: true
runtime:
  host: UNKNOWN
  agent_runtime: UNKNOWN
recovery:
  primary: REPLACE_WITH_REAL_RECOVERY_PATH_OR_UNKNOWN
rescue:
  primary: REPLACE_WITH_HUMAN_OR_AGENT_RESCUER
unknowns: []
```

The dates above are only an example. Choose a freshness window appropriate to the Host. The reference initializer starts with seven days; shorten or lengthen it when the environment changes at a different rate.

Set `minimum_ready: true` only after shared settings, one recovery path, and one rescuer are recorded. If no usable recovery path or rescuer exists, leave it false and record the gap.

### 5. Make the record expire

`SYSTEM.yaml` is not timeless truth.

Run `python tools/ena_preflight.py` at session/Agent/workspace start when the Host supports a startup hook. Refresh First Use when the file is past `valid_until`.

Before an important self-change, recheck the specific mutable recovery/startup/communication facts the change depends on even if `SYSTEM.yaml` has not yet expired.

## Expand the map only when a capability needs it

After the minimum is working, inspect additional areas as they become relevant instead of blocking adoption on a complete inventory.

### Communication / A2A

When configuring A2A, identify and verify the real two-way path, Agent Card/discovery record, transport/authentication, permissions and reachable peers. Reuse the existing A2A identity mechanism. See `A2A.md`.

### Memory / evolution

Before enabling Sleep/Dream, identify durable memory sources, experience/history, retrieval/indexing, write/update method, reversible history/snapshot, scheduler/idle/event triggers, and excluded sensitive sources. Do not create a second ENA memory database when the Host already has a suitable memory system.

### Recovery and risky self-change

Before important self-change, identify the exact affected surface, previous working state, rollback method and external recovery actor. See `SURVIVAL.md` and `SAFE-CHANGE.md`.

Additional useful facts may include Git/version control, backups, snapshots, logs, watchdogs, deployment rollback, working directories, mounts, credentials references and startup dependencies. Record unknowns explicitly rather than inventing completeness.

## First Use is minimally complete when

- timezone, language and ENA home are confirmed;
- `ENA.yaml` exists;
- `SYSTEM.yaml` has `checked_at`, `valid_until` and `minimum_ready: true`;
- one real recovery path is recorded;
- one human or Agent rescuer is recorded;
- unknown facts remain visible as `UNKNOWN` rather than being guessed.

Then continue with the capabilities actually needed on this Host.
