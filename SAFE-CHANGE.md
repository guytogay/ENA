# Safe self-change

Use this path for a change that could stop the Agent from starting, communicating, using required tools, or repairing itself.

The rule is simple:

> Preserve the previous working state, prepare recovery, arm an independent rollback, share the recovery instructions with another Agent, then make the change.

## One change, one recovery package

Before changing live state, create a package such as:

```text
~/.ena/changes/
  20260912T011530+0800__fix-a2a-channel/
    change.md
    rescue.yaml
    status.yaml
    backup/
    rollback.py | rollback.sh | rollback.ps1 | Host-native recovery reference
```

Use the timezone confirmed in `ENA.yaml`. Include seconds and the actual UTC offset in the package name.

Store the package somewhere that survives failure of the component being changed.

## Before the change

1. **Record the target.** List the exact files, services, packages, routes, configuration or other state that will change.
2. **Preserve the previous working state.** Use version control, a file backup, deployment revision, container image, filesystem/VM snapshot, database transaction, or another reliable Host-native mechanism.
3. **Prepare rollback.** Write the exact command/script/action that restores only this change. Verify that its files, permissions and restore point exist.
4. **Prepare `rescue.yaml`.** Give another Agent enough information to restore the target without reconstructing the incident from conversation history.
5. **Arm independent automatic rollback.** Normally use a 5–10 minute Host timer/scheduler that does not depend on the changed Agent remaining healthy.
6. **Send the recovery information to a rescue peer through A2A and receive acknowledgement for this exact package.**
7. Set `status.yaml` to `armed`.
8. Only then apply the live change and set the status to `applied`.

## What `rescue.yaml` needs

Keep it short and executable. Include the fields that apply on the current Host:

```text
target Agent / Agent Card
where recovery must run
package path or identifier
exact components changed
known-good backup/snapshot/version
exact rollback command or action
automatic rollback job and deadline
restart/reload action
how to verify communication is back
when the rescue peer is authorized to act
what the rescue peer must not modify
fallback restore point or human escalation
```

Refer to credentials; do not put secrets into the rescue file merely for convenience.

See `examples/change/RESCUE.example.yaml`.

## Package state

Keep one machine-readable current state in `status.yaml`:

```text
preparing   package is being prepared; live state is unchanged
armed       backup + rollback + timer + rescue acknowledgement are ready
applied     live change is active; automatic rollback remains armed
retained    communication is confirmed and rollback timer was cancelled
restoring   recovery is running
restored    previous working state is back and communication works
failed      prepared recovery did not restore usability
cancelled   change was abandoned before live mutation
```

Update the state atomically where the Host supports it. See `examples/change/STATUS.example.yaml`.

## After the change

Prove the Agent still has a usable communication path with a normal two-way human or A2A exchange.

If communication works:

```text
cancel automatic rollback
→ confirm cancellation
→ state = retained
```

If communication does not work:

```text
do not cancel rollback
→ allow the independent timer to restore
→ or let the acknowledged rescue peer execute the prepared rollback
```

A running process alone does not prove recovery.

## Avoid two rescuers corrupting the same state

The timer and rescue peer may act at nearly the same time. Make rollback idempotent when possible, or use an atomic lock/status check so the second recovery attempt detects that restoration has already happened.

A rollback should normally refuse destructive action when state is already `retained`, `restored`, or `cancelled` unless an explicit fallback procedure says otherwise.

## Keep the package

After completion, keep the package as change history. Archive old packages only when doing so does not remove a backup, restore reference, script or other dependency still needed by the current known-good state.

## Reference tool

`tools/change_scaffold.py` creates the timestamped package structure and starter files. It intentionally does not pretend to know the correct backup/rollback mechanism for every Host. Fill the package with the real Host-native backup, rollback and timer before changing live state.
