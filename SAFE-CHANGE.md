# Safe self-change

Use this path for a change that could stop the Agent from starting, communicating, using required tools, or repairing itself.

The invariant is simple:

> Before live change, preserve the previous working state and prepare a recovery path that survives failure of the current Agent/session.

The exact mechanism depends on the Host. Do not force a daemon-style timer/A2A design onto a session-based coding Agent.

## Choose the Host profile first

### Resident runtime

Examples: systemd service, long-running container, VM Agent, daemon or always-on worker.

Prefer:

- Host supervisor/restart outside the Agent process;
- snapshot/version/file backup;
- independent timed rollback when practical;
- a human or A2A Agent able to use the recovery package;
- external communication verification after the change.

For a consequential live mutation, a 5–10 minute independent rollback window is a useful starting mechanism when the Host supports it reliably.

### Session / coding Agent

Examples: Codex, Claude Code, terminal coding Agent, chat/tool session whose process is the current interaction.

Prefer:

- durable disk/repository state outside the current session;
- Git commit/branch/worktree/revert, file backup or another exact restore point before mutation;
- recovery instructions stored on disk;
- a new session and/or human operator as the external recovery path;
- repository/tests or human-visible communication as the post-change check.

A wall-clock rollback daemon and A2A peer are not required when the Host does not naturally provide them. Do not block safe work merely because those mechanisms are absent.

## A human is a valid rescuer

The recovery actor may be:

- a human with access to the Host/repository/recovery mechanism;
- another Agent through A2A;
- a Host-native external supervisor/rollback mechanism;
- a combination of these.

If an interactive human or Agent is expected to perform recovery, give that rescuer the exact package/location and obtain acknowledgement when practical. A2A acknowledgement is not a universal prerequisite on Hosts where A2A does not exist.

## One change, one recovery package

Before changing live state, create a package such as:

```text
~/.ena/changes/
  20260912T011530+0800__fix-channel/
    change.md
    rescue.yaml
    status.yaml
    backup/
    rollback.py | rollback.sh | rollback.ps1 | Host-native recovery reference
```

Use the timezone confirmed in `ENA.yaml`. Store the package somewhere that survives failure of the changed component/current session.

## Before the change

1. **Record the target.** List the exact files, services, packages, routes, configuration or other state that will change.
2. **Preserve the previous working state.** Use Git/worktree, a file backup, deployment revision, container image, filesystem/VM snapshot, database transaction, or another reliable Host-native mechanism.
3. **Prepare rollback.** Record the exact command/script/action that restores only this change. Verify the restore point exists.
4. **Prepare `rescue.yaml`.** Give the external recovery actor enough information to restore the target without reconstructing the incident from conversation history.
5. **Prepare the profile-specific external recovery path.**
   - resident runtime: normally arm an independent rollback timer/scheduler when available;
   - session/coding Agent: ensure the durable restore point and recovery instructions survive the session, and identify the human/new-session recovery path.
6. **Confirm the external recovery actor/path is usable.** Obtain human/Agent acknowledgement when that actor is expected to intervene interactively.
7. Set `status.yaml` to `armed`.
8. Only then apply the live change and set status to `applied`.

## What `rescue.yaml` needs

Keep it short and executable. Include what applies on this Host:

```text
target Agent/session/repository
Host profile: resident | session
where recovery must run
package path or identifier
exact components changed
known-good backup/snapshot/version/commit
exact rollback command or action
automatic rollback job and deadline, if one exists
restart/reload/new-session action
how to verify communication or useful operation is back
human / Agent / Host recovery actor
what the rescuer must not modify
fallback restore point or escalation
```

Refer to credentials; do not embed secrets merely for convenience. See `examples/change/RESCUE.example.yaml`.

## Package state

Keep one machine-readable current state in `status.yaml`:

```text
preparing   recovery package is incomplete; live state is unchanged
armed       restore point + recovery path are ready for this Host profile
applied     live change is active; recovery remains available
retained    post-change usefulness/communication check passed; new state is kept
restoring   recovery is running
restored    previous working state is back and useful operation/communication works
failed      prepared recovery did not restore usability
cancelled   change was abandoned before live mutation
```

A resident runtime with a rollback timer cancels that timer only after the post-change check succeeds. A session Agent without such a timer simply records `retained` after the corresponding repository/test/human communication check succeeds.

A running process alone does not prove recovery.

## Avoid two rescuers corrupting the same state

When more than one recovery actor can act, make rollback idempotent where possible or use an atomic lock/status check so a second recovery attempt detects that restoration has already happened.

A rollback should normally refuse destructive action when state is already `retained`, `restored`, or `cancelled` unless an explicit fallback says otherwise.

## Keep the package

Keep the completed package as change history. Archive it only when doing so does not remove a restore dependency still needed by the current known-good state.

`tools/change_scaffold.py` creates the package skeleton. Fill it with the real Host-native restore path before changing live state.
