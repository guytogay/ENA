# First Use

First Use has two jobs:

1. inspect the Agent and Host as they actually exist;
2. normalize the settings later ENA functions will share.

Verify facts from the Host, runtime, files, tools, APIs, documentation or other available evidence. Do not guess when the environment can be inspected.

## 1. Inspect the runtime

Identify:

- Agent runtime and Host;
- model/model service when exposed;
- available tools, plugins, APIs, shell/code execution, browser and schedulers;
- startup, stop, restart and supervision mechanisms;
- important working directories, mounts, configuration and dependencies.

Record how important facts were verified.

## 2. Confirm one timezone

Inspect the timezone used by the operating system, runtime, scheduler, logs, databases and relevant applications when exposed.

Ask the user to confirm the canonical timezone. Suggest `Asia/Shanghai` by default unless the user chooses another IANA timezone such as `America/Los_Angeles`.

Also check whether the Host clock is reasonably synchronized.

After confirmation:

- use this timezone for ENA timestamps, schedules, deadlines, recovery records and evolution records;
- use the actual UTC offset in event timestamps where useful;
- align Agent-controlled components when safe;
- record explicit conversion boundaries for components that must use another timezone.

## 3. Confirm one working language

Ask the user to confirm the language used for ENA records and operational Agent-to-Agent messages. Store a normal language tag such as `zh-CN` or `en-US`.

Keep commands, paths, identifiers, API fields and protocol payloads in the exact form required by the underlying system.

Use UTF-8 for ENA-owned text files unless an external interface requires another encoding.

## 4. Confirm the ENA home

Ask where ENA-owned files should live. If there is no preference, use a stable directory under the Agent user's home, for example:

```text
~/.ena/
```

Create only what is needed. A typical installation may become:

```text
~/.ena/
  ENA.yaml
  SYSTEM.yaml
  changes/
  evolution/
```

## 5. Verify communication

Identify and test:

- how humans reach the Agent;
- whether A2A already exists;
- the Agent Card or other discovery record used by the A2A implementation;
- at least one real two-way A2A exchange;
- transport, authentication and permissions;
- at least one reachable rescue peer when the Host can support it.

Reuse the existing A2A identity/discovery mechanism. Do not create a second ENA identity system.

See `A2A.md`.

## 6. Inspect memory

Identify how the Agent actually retains and retrieves information across sessions/restarts:

- durable memory sources;
- conversation/task/episodic history that can supply experience;
- semantic/vector/indexed retrieval;
- persistent procedures, skills or preferences;
- how durable memory is written or updated;
- how a mistaken update can be versioned, reversed, restored or superseded;
- schedulers, idle hooks or event triggers that can run maintenance;
- memory sources that must be excluded from consolidation or recombination.

Do not create a separate ENA memory database when the Host already has a suitable memory system.

## 7. Inspect backup and recovery

Find the Host mechanisms already available:

- Git or other version control;
- file, volume, container, VM or database snapshots;
- backup/restore tools;
- service restart mechanisms;
- task schedulers/timers;
- watchdogs and health checks;
- deployment/release rollback;
- logs.

Prefer reliable Host-native mechanisms.

## 8. Identify risky self-change surfaces

List the parts whose modification could stop the Agent from starting, communicating, using required tools or repairing itself.

For each important surface, identify:

- what can change;
- where the previous working state can be preserved;
- how the change can be reversed;
- what independent mechanism can still execute recovery if the Agent becomes unreachable.

See `SAFE-CHANGE.md`.

## 9. Write two durable records

### `ENA.yaml`

Keep user-confirmed shared settings and stable pointers.

Minimum:

```yaml
ena_home: ~/.ena
canonical_timezone: Asia/Shanghai
canonical_language: zh-CN
text_encoding: UTF-8
```

Use `ENA.example.yaml` as a starting point.

### `SYSTEM.yaml`

Record the verified runtime, capabilities, communication, memory, recovery mechanisms, risky change surfaces and important unknowns.

This is a current system map, not timeless truth. Recheck mutable facts before consequential changes.

Use `examples/SYSTEM.example.yaml` as a starting point.

## First Use is complete when

- the user has confirmed timezone, language and ENA home;
- `ENA.yaml` exists;
- `SYSTEM.yaml` describes verified runtime, communication, memory and recovery facts;
- human communication is known;
- A2A is verified/established or its absence is recorded;
- restart, backup/snapshot and scheduler/timer mechanisms are known or their absence is recorded;
- risky self-change surfaces and recovery limits are visible.

Then continue with:

```text
A2A.md
→ SURVIVAL.md
→ SAFE-CHANGE.md
→ EVOLUTION.md
→ SLEEP-DREAM-QUICKSTART.md
```
