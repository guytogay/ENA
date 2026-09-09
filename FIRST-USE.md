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

## 2. Establish one canonical timezone

Inspect the time settings used by the Host and the components the Agent depends on, including the operating system, runtime, schedulers, logs, databases, and relevant applications where exposed.

Ask the user to confirm the canonical timezone to use. Default to `Asia/Shanghai` unless the user chooses another timezone.

Store the choice as an IANA timezone name, for example:

```text
Asia/Shanghai
America/Los_Angeles
Europe/Rome
```

After confirmation:

- use the canonical timezone for all ENA timestamps, records, schedules, deadlines, change packages, recovery information, and evolution history;
- align Agent-controlled components to the same timezone where this can be done safely;
- record any component that must remain on another timezone and the conversion boundary;
- include the actual UTC offset in individual timestamps when it helps make the time unambiguous.

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
- use this location as the stable entry point for ENA-owned ACMS, change, A2A, recovery, and evolution records;
- record any ENA data that must live elsewhere as an explicit path from `ENA.yaml` rather than relying on rediscovery.

A typical layout may begin as:

```text
~/.ena/
  ENA.yaml
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

## 6. Verify communication paths

Verify, rather than merely list:

- how humans can reach you;
- which other Agents you can reach;
- whether real bidirectional A2A communication works;
- what transport, authentication, and permissions those channels depend on.

If no A2A path exists and the Host provides enough capability to create one, establish a practical A2A path.

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

Record the places where a self-change could affect your ability to keep operating or repair yourself.

For each important surface, determine:

- what can be changed;
- where the previous working state can be preserved;
- how that specific change can be reversed;
- what independent mechanism can still execute the reversal if the main Agent becomes unresponsive.

## 9. Write the durable ENA configuration

Persist the confirmed shared settings in `ENA.yaml` at the ENA home so later capabilities do not have to ask or infer them again.

At minimum, record:

```yaml
ena_home: ~/.ena
canonical_timezone: Asia/Shanghai
canonical_language: zh-CN
```

Replace the example values with the values confirmed by the user and store `ena_home` in the Host-appropriate form.

The same configuration may also record stable pointers discovered during First Use, such as:

- runtime / Host identity;
- startup / restart path;
- human communication path;
- A2A path;
- ACMS location;
- available backup / snapshot / versioning mechanisms;
- available independent timer / scheduler for automatic rollback;
- known way to restore each critical change surface;
- important unknowns that could not be inspected.

Record how important facts were verified when that will help them be checked again later. Re-check mutable facts before a consequential self-change.

## What happens next

Once the Agent has inspected and normalized its operating environment:

1. establish or verify A2A;
2. build a change/recovery mechanism appropriate to the Host;
3. before a body-changing operation, preserve the previous state, record the intended change and rollback method, arm an independent timed rollback, and send the recovery information to another Agent;
4. apply the change;
5. after the change, confirm a normal bidirectional conversation with a human or another Agent;
6. if communication is normal, cancel the pending automatic rollback;
7. if the Agent becomes unreachable, allow the independent timer to restore the previous state or let another Agent use the recovery information already supplied.

Use the confirmed ENA home, canonical timezone, and canonical language throughout these operations.