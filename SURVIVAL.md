# Survive failure

Build a recovery path that remains available when the Agent process is crashed, unreachable, or unable to repair itself.

Prefer reliable Host-native supervision and recovery mechanisms. Keep recovery controls outside the component they protect.

## 1. Make restart possible without the Agent

Identify/configure the Host mechanism that can start and restart the Agent without requiring the Agent to be healthy first.

Examples:

- service manager;
- process supervisor;
- container/orchestrator restart policy;
- VM supervisor;
- another Host-native restart mechanism.

Record in `SYSTEM.yaml`:

- start/stop/restart actions;
- the external component that performs them;
- whether the Agent returns after Host reboot or process failure.

Enable automatic restart for ordinary process failure when appropriate.

## 2. Keep an external communication check

A running process does not prove the Agent is usable.

Use the smallest reliable external check available. A successful normal two-way human or A2A exchange is sufficient evidence that a rescue channel exists.

A lower-level process/service health check can help with detection, but do not place the only health check inside the Agent being checked.

## 3. Use this recovery order

```text
probe again once
→ restart the Agent
→ verify communication
→ if still unreachable, restore the most relevant known-good state
→ restart/reload as required
→ verify communication again
→ if still unreachable, use the rescue peer or human/external recovery
```

The second probe avoids reacting to a transient miss.

## 4. Restore the smallest relevant state

If failure follows a recent package from `SAFE-CHANGE.md`, use that package's prepared rollback before restoring unrelated state.

Otherwise use the known-good recovery mechanism recorded during First Use, such as:

- service-definition backup;
- deployment revision;
- file/volume snapshot;
- container image;
- VM snapshot;
- another verified restore point.

Prefer a smaller reliable recovery over an unnecessarily broad old snapshot.

## 5. Keep recovery outside the same failure path

Where possible:

- keep restart/supervisor control outside the Agent process;
- keep automatic rollback outside the component being changed;
- keep recovery packages on storage that survives failure of the target service/container/process;
- keep at least one rescue peer outside the target Agent;
- do not change the only communication path and its only recovery path in the same operation.

## 6. Keep `SYSTEM.yaml` current

Record the recovery mechanisms currently available:

- supervisor/service manager;
- restart action;
- communication check;
- latest unresolved safe-change package, if any;
- backup/snapshot/version restore points;
- rescue peer;
- human/external escalation path;
- known limitations.

When a retained change alters startup, service names, runtime location, A2A endpoint, recovery storage or scheduler, update the system record.
