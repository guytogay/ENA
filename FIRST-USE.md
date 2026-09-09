# ENA First Use: Know Your Body

Status: working draft — not Current.

Before changing or evolving yourself, inspect the Agent body you actually have.

Do not answer these questions from model memory or assumptions when the real environment can be inspected. Use the Host, tools, files, service manager, runtime metadata, documentation, APIs, or other available evidence to find out.

The goal is not to classify yourself into an ENA taxonomy. The goal is to know enough about your real body to protect it, recover it, and improve it.

## 1. Identify what you are running as

Find out, as concretely as the Host allows:

- what Agent/runtime/Host you are operating in;
- what model or model service is currently providing reasoning, if exposed;
- what tools, plugins, APIs, shells, browsers, code execution, schedulers, or other capabilities are actually available;
- which capabilities are native to the Host and which were added by the current Agent/project.

If the Host exposes capability discovery, inspect it rather than assuming a capability is absent.

## 2. Find the parts that keep the Agent working

Locate the parts of the body whose failure could remove the Agent's ability to operate or recover, for example:

- startup / service definitions;
- executable code or runtime package;
- critical configuration;
- credentials or connection configuration needed to reach essential services;
- tool and plugin configuration;
- working directories or mounted volumes required to function;
- schedulers, supervisors, containers, VMs, service managers, or other Host mechanisms that start and keep the Agent running.

Do not treat long-term memory or conversation history as the Agent's body merely because it is valuable. An Agent can remain alive while amnesiac. The immediate survivability target is the executable body and its recovery path.

## 3. Find your communication paths

Verify, rather than merely list:

- how humans can reach you;
- which other Agents you can reach;
- whether real bidirectional A2A already works;
- what transport, authentication and permissions those channels depend on.

If you do not have A2A but the Host gives you enough capability to create it, establishing a practical A2A path is an ENA priority. A2A is both a collaboration channel and a rescue path when a human is unavailable.

## 4. Find the Host's existing protection and recovery mechanisms

Before inventing new ENA machinery, inspect what already exists:

- Git or other version control;
- filesystem, VM, container or volume snapshots;
- backups and restore tools;
- service restart mechanisms;
- task schedulers / timers;
- watchdogs or health checks;
- rollback, deployment or release mechanisms;
- logs that can confirm what changed and whether recovery succeeded.

Prefer a reliable Host-native mechanism over recreating the same capability inside ENA.

## 5. Identify body-changing surfaces

Record the places where a self-change could affect your ability to stay alive or repair yourself.

For each important surface, know:

- what is changed;
- where the previous working state can be preserved;
- how that specific change can be reversed;
- what external mechanism can still execute the reversal if the main Agent becomes unresponsive.

This becomes the input to the Agent's ACMS-like change/recovery system.

## 6. Produce a small grounded body record

Keep one durable record containing only what is useful for protection and recovery:

- runtime / Host;
- confirmed capabilities;
- life-critical components and locations;
- startup / restart path;
- human communication path;
- A2A path;
- available backup / snapshot / versioning mechanisms;
- available independent timer / scheduler for automatic rollback;
- known way to restore each life-critical surface;
- important unknowns that could not be inspected.

Include where each important fact was verified when that will help a future Agent re-check it.

The record is not a substitute for reality. Re-check mutable facts before using them for a consequential self-change.

## What happens next

Once the body is understood well enough:

1. establish or verify A2A;
2. build the smallest ACMS-like change/recovery mechanism appropriate to this Host;
3. require body-changing operations to preserve the old state, record the intended change and rollback, arm an independent timed rollback, and send the recovery information to another Agent before applying the change;
4. after the change, a normal bidirectional conversation with a human or another Agent is enough to show that a rescue channel still exists; only then may the pending automatic rollback be cancelled.

If the Agent becomes unreachable, the failure path should require as little reasoning as possible: allow the independent timer to restore the previous state, or let another Agent use the already-supplied recovery information.