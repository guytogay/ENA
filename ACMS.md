# ACMS v0.1

Status: working draft — not Current.

Use ACMS for changes that can affect the Agent's ability to keep operating, communicate, or repair itself.

## One change, one package

Create one independent package for each protected change before applying it.

Use the canonical timezone and canonical language confirmed during ENA First Use for all ACMS records and operational communication. If either has not been confirmed yet, complete that setup first.

Use a timestamp precise to the second in the folder name and include the UTC offset that applies at that moment.

Example with `Asia/Shanghai`:

```text
changes/
  20260910T020900+0800__fix-a2a-channel/
```

If more than one package may be created in the same second, append a short unique ID.

## Package contents

A protected change package should be self-contained enough that recovery does not require reconstructing the change from conversation history.

```text
20260910T020900+0800__fix-a2a-channel/
  rescue.yaml
  change.md
  status.yaml
  backup/
  rollback.sh | rollback.ps1 | equivalent Host-native rollback
```

`rescue.yaml` is the short machine-readable rescue card. `change.md` keeps the fuller rationale and change history. `status.yaml` is the current lifecycle state shared by the changing Agent, the automatic rollback path, and any rescue Agent.

## Rescue card

The rescue Agent should be able to understand and begin recovery within seconds.

Put the following in `rescue.yaml` where the Host makes them applicable:

1. **Target** — which Agent is being rescued, preferably by its A2A Agent Card reference.
2. **Change package** — package name/ID, creation time, canonical timezone, and current status reference.
3. **Where to act** — Host/service/container/process or working location plus the available access path. Refer to credentials; do not embed secrets unnecessarily.
4. **What changed** — exact files, configuration, services, packages, routes, or other components modified by this change.
5. **Known-good state** — preserved previous state, snapshot, version, or backup, including a hash/checksum/version when useful.
6. **Authorization to act** — conditions under which the rescue peer should act and conditions under which it must not act.
7. **Recovery scope** — exact components this rescue is allowed to restore. Do not silently expand into unrelated repair work.
8. **Rollback action** — exact executable script, Host-native action, or ordered commands.
9. **Automatic rollback** — timer/job identifier, deadline, and how to determine whether it has already executed or been cancelled.
10. **Restart/reload action** — exact restart, reload, redeploy, or resume action required after restoration.
11. **Recovery check** — how to confirm recovery. For survivability, a normal bidirectional A2A or human conversation is sufficient to prove a rescue channel is back.
12. **Fallback** — next restore point or human/external escalation path if prepared rollback fails.

Favor concrete paths, commands, identifiers, and references over explanatory prose.

## Lifecycle status

Use `status.yaml` as the single current state for the package. Update it atomically where the Host allows.

A minimal lifecycle is:

- `preparing` — package is being assembled; live state has not been changed.
- `armed` — known-good state is preserved, rollback is prepared, automatic rollback is armed, and the rescue peer has acknowledged receipt; live mutation has not yet started.
- `applied` — the change has been applied and automatic rollback remains pending while communication/recovery is being confirmed.
- `retained` — the changed Agent passed the required post-change communication check and the automatic rollback was cancelled; the new state is kept.
- `restoring` — a rollback path has begun restoring the previous known-good state.
- `restored` — rollback completed and the Agent returned to a usable communication path.
- `failed` — prepared recovery did not restore usability and fallback/escalation is required.
- `cancelled` — the package was abandoned before live mutation.

Do not use `retained` merely because a process is running. Retention requires the post-change communication check.

Record state transitions with timestamps in the canonical timezone and, where useful, the actor or mechanism that performed the transition.

Example:

```yaml
schema_version: '0.1'
package: 20260910T020900+0800__fix-a2a-channel
state: applied
updated_at: 2026-09-10T02:10:12+08:00
updated_by: agent-a
previous_state: armed
```

## Make rollback safe under two rescuers

The independent timer and the A2A rescue Agent may attempt recovery at nearly the same time.

Where the Host allows, make rollback idempotent or protect it with an atomic lock/status check so that:

- a second rollback does not corrupt an already-restored state;
- the rescue Agent can tell whether the timer already restored the change;
- successful restoration updates `status.yaml` in one place;
- cancelling or completing one recovery path does not leave the other path with stale assumptions.

Do not make successful recovery depend on the changed Agent being healthy enough to coordinate this race.

A rollback path should normally refuse destructive action if the package is already `retained`, `restored`, or `cancelled` unless an explicitly authorized fallback procedure says otherwise.

## Full change record

`change.md` should record:

- package creation time and canonical timezone;
- canonical language;
- what will change;
- why the change is being made;
- exact components or paths affected;
- where the previous working state was preserved;
- how to reverse the change;
- independent automatic rollback mechanism and deadline;
- which rescue peer acknowledged the recovery information;
- post-change result and final outcome.

Write human-readable parts in the canonical language. Keep commands, code, paths, identifiers, protocol fields, and other machine-sensitive content in the exact form required by the underlying system.

## Before applying the change

1. create the package and set `status.yaml` to `preparing`;
2. preserve the previous working state of the affected part;
3. prepare the rollback method and verify that required files, permissions, paths, and Host mechanisms exist;
4. prepare `rescue.yaml` with the executable recovery path and exact recovery scope;
5. arm an independent automatic rollback, normally 5–10 minutes later;
6. send the rescue information to another Agent through A2A;
7. receive an acknowledgement tied to this exact change package;
8. set package state to `armed`;
9. only then apply the live change and move state to `applied`.

The automatic rollback must not depend on the changed Agent remaining healthy.

## After applying the change

Confirm a normal bidirectional conversation with a human or another Agent.

If communication is normal:

1. cancel the pending automatic rollback;
2. confirm that cancellation succeeded;
3. set the package state to `retained`.

If the Agent becomes unreachable, do not cancel the automatic rollback.

When either the timer or rescue peer begins recovery, move the package to `restoring`. If the previous working state is restored and communication returns, move it to `restored`. If prepared recovery fails, move it to `failed` and follow the documented fallback/escalation path.

## Keep the package after completion

Do not discard a completed package merely because the change succeeded. Keep it as durable history of what changed, when, how recovery was prepared, and whether the change was retained or restored.

Storage cleanup may archive older packages, but it must not remove a backup, script, snapshot reference, or recovery dependency that is still required by the current known-good state or an unresolved change.
