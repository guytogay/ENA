# ENA First Use: Inspect and Normalize

Status: working draft — not Current.

First Use has two jobs:

1. **Inspect** the environment the Agent actually runs in.
2. **Normalize** the shared operating conventions that later ENA capabilities will rely on.

Verify facts from the Host, tools, files, runtime metadata, documentation, APIs, or other available evidence rather than relying on assumptions.

## 1. Identify your runtime and capabilities

Find out, as concretely as the Host allows:

- what Agent/runtime/Host you are operating in;
- what model or model service is providing reasoning, if exposed;
- what tools, plugins, APIs, shells, browsers, code execution, schedulers, or other capabilities are available;
- which capabilities are native to the Host and which were added by the current Agent or project.

If the Host provides capability discovery, inspect it directly.

## 2. Establish one canonical timezone and verify the clock

Inspect the time settings used by the Host and the components the Agent depends on, including the operating system, runtime, schedulers, logs, databases, and relevant applications where exposed.

Ask the user to confirm the canonical timezone to use. Default to `Asia/Shanghai` unless the user chooses another timezone.

Store the choice as an IANA timezone name, for example:

```text
Asia/Shanghai
America/Los_Angeles
Europe/Rome
```

Also verify that the Host clock is reasonably synchronized using the time service available on that Host. Timed rollback depends on trustworthy time, not only a timezone label.

After confirmation:

- use the canonical timezone for all ENA timestamps, records, schedules, deadlines, change packages, recovery information, and evolution history;
- align Agent-controlled components to the same timezone where this can be done safely;
- record any component that must remain on another timezone and the conversion boundary;
- include the actual UTC offset in individual timestamps when it helps make the time unambiguous;
- record the Host clock synchronization mechanism or any known clock-reliability limitation.

Do not mix timezones silently inside the Agent's operating records.

## 3. Establish one canonical language

Ask the user to confirm the working language the Agent should use for ENA records and Agent-to-Agent operational communication. The language currently used with the user may be offered as the initial suggestion, but the user should confirm it.

Store the choice as a standard language tag where practical, for example:

```text
zh-CN
en-US
it-IT
```

After confirmation, use the canonical language consistently for:

- ENA operating records;
- ACMS change descriptions and recovery guides;
- A2A operational messages and rescue instructions;
- evolution records, findings, and retained lessons;
- user-facing ENA status and recovery information.

Keep code, commands, file paths, identifiers, API field names, protocol payloads, and other machine-defined content in the form required by the underlying system. Translate or explain surrounding text when needed, but do not alter machine-sensitive content merely to match the canonical language.

Use UTF-8 for ENA-owned YAML, Markdown, and other text records unless the Host requires another encoding for a specific external interface.

Record any interface or collaborator that requires another language and handle that as an explicit translation boundary rather than silently mixing languages in the Agent's durable records.

## 4. Establish one ENA home directory

Ask the user to confirm where ENA's own durable files should live on this Host. If the user has no preference, use a stable directory under the Agent user's home, for example:

```text
~/.ena/
```

Use the Host-equivalent user-home path where `~` is not appropriate.

After confirmation:

- create the ENA home if it does not already exist;
- keep `ENA.yaml` at the root of this directory;
- keep the grounded body record at `BODY.yaml` unless the Host requires another explicit location;
- use this location as the stable entry point for ENA-owned ACMS, change, A2A, recovery, and evolution records;
- record any ENA data that must live elsewhere as an explicit path from `ENA.yaml` rather than relying on rediscovery.

A typical layout may begin as:

```text
~/.ena/
  ENA.yaml
  BODY.yaml
  acms/
  changes/
  a2a/
  evolution/
```

Create only the directories that are actually needed on the current Host.

## 5. Find the components required to keep operating

Locate the components required to start, communicate, act, and recover, for example:

- startup or service definitions;
- executable code or runtime package;
- critical configuration;
- credentials or connection configuration needed for essential services;
- tool and plugin configuration;
- working directories or mounted volumes required to function;
- schedulers, supervisors, containers, VMs, service managers, or other Host mechanisms that start and keep the Agent running.

For important findings, record how they were verified so a later Agent can re-check them without guessing.

## 6. Verify communication and A2A

Verify, rather than merely list:

- how humans can reach you;
- whether a standards-based or Host-native A2A path already exists;
- which other Agents can be reached;
- whether a real bidirectional A2A exchange works;
- what transport, authentication, and permissions those channels depend on;
- where the Agent's A2A Agent Card or equivalent discovery record can be retrieved, when applicable.

If A2A already exists, reuse its identity/discovery mechanism rather than creating a parallel ENA identity.

If no A2A path exists and the Host provides enough capability to create one, establish a practical A2A path and at least one reachable rescue peer. See [`A2A.md`](A2A.md).

## 7. Find existing protection and recovery mechanisms

Inspect what the Host already provides:

- Git or other version control;
- filesystem, VM, container, or volume snapshots;
- backups and restore tools;
- service restart mechanisms;
- task schedulers or timers;
- watchdogs or health checks;
- rollback, deployment, or release mechanisms;
- logs that can confirm what changed and whether recovery succeeded.

Reuse reliable Host-native mechanisms where possible.

## 8. Identify body-changing surfaces

Record the places where a self-change could affect the Agent's ability to keep operating or repair itself.

For each important surface, determine:

- what can be changed;
- where the previous working state can be preserved;
- how that specific change can be reversed;
- what independent mechanism can still execute the reversal if the main Agent becomes unresponsive.

## 9. Write the durable First Use outputs

First Use should leave two durable entry records.

### `ENA.yaml`

Store confirmed operating conventions and stable pointers used by later ENA capabilities.

At minimum:

```yaml
ena_home: ~/.ena
canonical_timezone: Asia/Shanghai
canonical_language: zh-CN
text_encoding: UTF-8
```

Replace example values with the user's confirmed choices and store `ena_home` in the Host-appropriate form.

`ENA.yaml` may also keep stable pointers to runtime controls, A2A Agent Card/rescue peers, survivability controls, ACMS, rollback scheduler, backups/snapshots, and evolution records. See [`ENA.example.yaml`](ENA.example.yaml).

### `BODY.yaml`

Store the grounded result of the actual inspection: runtime, confirmed capabilities, critical components and locations, communication paths, Host recovery mechanisms, body-changing surfaces, clock synchronization, verification evidence, and important unknowns.

Do not treat `BODY.yaml` as timeless truth. Re-check mutable facts before a consequential self-change. See [`examples/BODY.example.yaml`](examples/BODY.example.yaml).

## First Use is complete when

- the user has confirmed the canonical timezone, canonical language, and ENA home;
- the Host clock/synchronization state has been checked;
- `ENA.yaml` exists at the confirmed ENA home;
- `BODY.yaml` contains grounded runtime, communication, recovery, and critical-component findings rather than assumptions;
- the human communication path has been identified;
- A2A has either been verified/established with a usable rescue peer or the missing capability is explicitly recorded;
- restart, backup/snapshot, scheduler/timer, and other Host recovery mechanisms have been identified or their absence recorded;
- important body-changing surfaces and known recovery limitations are visible to later ENA capabilities.

## What happens next

Once the Agent has inspected and normalized its operating environment:

1. establish or verify the practical A2A path and rescue peer in [`A2A.md`](A2A.md);
2. build the external restart/recovery ladder in [`SURVIVAL.md`](SURVIVAL.md);
3. build the protected change/recovery mechanism in [`ACMS.md`](ACMS.md);
4. route body-changing operations through ACMS;
5. use [`EVOLUTION.md`](EVOLUTION.md) to turn useful improvement candidates into observed, retainable, reversible change.

Use the confirmed ENA home, canonical timezone, canonical language, and grounded body record throughout these operations.
