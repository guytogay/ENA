# ENA First Use: Inspect Your Agent

Status: working draft — not Current.

Before changing or evolving yourself, inspect the environment you actually run in. Verify facts from the Host, tools, files, runtime metadata, documentation, APIs, or other available evidence rather than relying on assumptions.

## 1. Identify your runtime and capabilities

Find out, as concretely as the Host allows:

- what Agent/runtime/Host you are operating in;
- what model or model service is providing reasoning, if exposed;
- what tools, plugins, APIs, shells, browsers, code execution, schedulers, or other capabilities are available;
- which capabilities are native to the Host and which were added by the current Agent or project.

If the Host provides capability discovery, inspect it directly.

## 2. Find the components required to keep operating

Locate the components required to start, communicate, act, and recover, for example:

- startup or service definitions;
- executable code or runtime package;
- critical configuration;
- credentials or connection configuration needed for essential services;
- tool and plugin configuration;
- working directories or mounted volumes required to function;
- schedulers, supervisors, containers, VMs, service managers, or other Host mechanisms that start and keep the Agent running.

## 3. Verify communication paths

Verify, rather than merely list:

- how humans can reach you;
- which other Agents you can reach;
- whether real bidirectional A2A communication works;
- what transport, authentication, and permissions those channels depend on.

If no A2A path exists and the Host provides enough capability to create one, establish a practical A2A path.

## 4. Find existing protection and recovery mechanisms

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

## 5. Identify body-changing surfaces

Record the places where a self-change could affect your ability to keep operating or repair yourself.

For each important surface, determine:

- what can be changed;
- where the previous working state can be preserved;
- how that specific change can be reversed;
- what independent mechanism can still execute the reversal if the main Agent becomes unresponsive.

## 6. Keep a grounded body record

Keep one durable record containing the information needed for protection and recovery:

- runtime / Host;
- confirmed capabilities;
- critical components and locations;
- startup / restart path;
- human communication path;
- A2A path;
- available backup / snapshot / versioning mechanisms;
- available independent timer / scheduler for automatic rollback;
- known way to restore each critical change surface;
- important unknowns that could not be inspected.

Record how important facts were verified when that will help them be checked again later. Re-check mutable facts before a consequential self-change.

## What happens next

Once the environment is understood well enough:

1. establish or verify A2A;
2. build a change/recovery mechanism appropriate to the Host;
3. before a body-changing operation, preserve the previous state, record the intended change and rollback method, arm an independent timed rollback, and send the recovery information to another Agent;
4. apply the change;
5. after the change, confirm a normal bidirectional conversation with a human or another Agent;
6. if communication is normal, cancel the pending automatic rollback;
7. if the Agent becomes unreachable, allow the independent timer to restore the previous state or let another Agent use the recovery information already supplied.