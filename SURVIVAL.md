# ENA Survivable Runtime

Status: working draft — not Current.

Build a recovery path that remains available when the main Agent is crashed, unreachable, or unable to repair itself.

Use Host-native supervision and recovery mechanisms where they are reliable. The recovery path should sit outside the failure surface of the Agent it is protecting.

## 1. Make the Agent startable without the Agent

Identify and configure the Host mechanism that can start and restart the Agent without requiring the Agent to be healthy first.

Examples include a service manager, container/orchestrator restart policy, VM supervisor, process supervisor, or another Host-native mechanism.

Record in `BODY.yaml`:

- how the Agent starts;
- how it stops;
- how it restarts;
- what external component performs those actions;
- whether the Agent returns automatically after Host reboot or process failure.

Where appropriate, enable automatic restart for ordinary process failure.

## 2. Keep a simple external reachability check

The external recovery path needs a way to distinguish an ordinary healthy Agent from one that has lost its usable communication path.

Prefer the smallest reliable check available on the Host. For ENA survivability, a successful normal bidirectional exchange with a human-facing or A2A path is sufficient evidence that a rescue channel exists.

A lower-level service/process health check may be useful for early detection, but a running process alone does not prove the Agent can communicate.

Do not put the only reachability check inside the Agent being checked.

## 3. Use a recovery ladder

When the Agent appears unreachable:

```text
probe again once
      ↓
restart the Agent
      ↓
verify communication
      ↓
if still unreachable, restore the most relevant known-good state
      ↓
restart/reload as required
      ↓
verify communication again
      ↓
if still unreachable, invoke A2A rescue or human/external escalation
```

The second probe avoids reacting to a transient miss. Keep the ladder simple enough that an external mechanism or rescue Agent can follow it without reconstructing the entire Agent.

## 4. Prefer the most local safe rollback

If the failure follows a recent ACMS-protected change, use that change package's prepared rollback before restoring unrelated parts of the Agent.

If there is no relevant ACMS package, use the Host's known-good recovery mechanism recorded during First Use, such as a service definition backup, deployment revision, filesystem snapshot, container image, VM snapshot, or other verified restore point.

Do not overwrite unrelated current state merely because a broad old snapshot exists when a smaller reliable recovery is available.

## 5. Keep the rescue path outside the failure domain

A recovery mechanism is not useful if the same change that kills the Agent also kills the recovery mechanism.

Where the Host allows:

- keep supervisor/restart control outside the Agent process;
- keep ACMS rollback timers outside the changed component;
- keep recovery packages on storage that survives the target service/container/process failure;
- keep at least one A2A rescue peer outside the target Agent;
- avoid changing the only communication path and its only recovery path in the same operation.

## 6. Record the current known-good recovery surface

`BODY.yaml` should identify the actual recovery mechanisms currently available, including:

- supervisor/service manager;
- restart command or action;
- communication verification path;
- ACMS location and current unresolved package, if any;
- backup/snapshot/version restore points;
- A2A rescue peer;
- external/human escalation path;
- known recovery limitations.

Re-check mutable recovery facts before a consequential body change.

## 7. Update recovery after structural change

When a retained change alters startup, service names, runtime location, A2A endpoint, recovery storage, scheduler, or another part of the recovery surface, update `BODY.yaml` and the relevant ENA pointers.

A survivability mechanism that still points at the old body is not a working recovery path.
