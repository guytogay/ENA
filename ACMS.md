# ACMS v0.1

Status: working draft — not Current.

Use ACMS for changes that can affect the Agent's ability to keep operating, communicate, or repair itself.

## One change, one package

Create one independent package for each change before applying it.

Use the canonical timezone and canonical language confirmed during ENA First Use for all ACMS records and operational communication. If either has not been confirmed yet, complete that setup before creating a change package.

The default canonical timezone is `Asia/Shanghai`; adopters may choose another IANA timezone during first use.

Use a timestamp precise to the second in the folder name and include the UTC offset that applies at that moment.

Example with `Asia/Shanghai`:

```text
changes/
  20260910T020900+0800__fix-agent-channel/
```

If more than one package may be created in the same second, append a short unique ID:

```text
changes/
  20260910T020900+0800__a4f2__fix-agent-channel/
```

## Package contents

Each package should contain enough information and material to reverse the change without first having to investigate what happened.

A minimal package can contain:

```text
rescue.yaml
change.md
backup/
rollback.sh | rollback.ps1 | equivalent Host-native rollback
status
```

`rescue.yaml` is the fast rescue contract for another Agent. Keep it short, structured, and directly actionable. `change.md` keeps the fuller change history and rationale.

A human-readable `RESCUE.md` may be generated or included when useful, but it should not be the only recovery artifact when another Agent is expected to act programmatically.

See [`examples/acms/RESCUE.example.yaml`](examples/acms/RESCUE.example.yaml).

## What the rescue Agent must know first

Put these items in `rescue.yaml` in a stable structure:

1. **Target** — which Agent is being rescued, preferably by its A2A Agent Card reference, plus the Host/service/process where recovery must occur.
2. **Change package** — package name/ID, creation time, canonical timezone, and current status.
3. **Authorization to act** — the concrete conditions under which the rescue Agent should begin recovery, and conditions under which it must not act.
4. **Scope** — exactly which changed components may be restored. Recovery should not overwrite unrelated state.
5. **Access path** — how to reach the Host or recovery surface. Refer to credential/authorization mechanisms; do not embed secrets unnecessarily.
6. **Known-good state** — where the preserved previous state, snapshot, version, or backup is located, including a version/hash/checksum when useful.
7. **Rollback action** — the exact rollback command, script, Host-native action, or ordered commands to execute. Prefer an already-prepared executable rollback over prose instructions.
8. **Automatic rollback** — whether an independent rollback is armed, its timer/job identifier, deadline, and how to determine whether it has already executed or been cancelled.
9. **Restart/reload action** — the exact restart, reload, redeploy, or resume action required after restoration, if any.
10. **Recovery check** — how to confirm recovery. For the ENA survivability case, restore the service if needed and confirm a normal bidirectional A2A or human conversation.
11. **Fallback** — what to try next if the prepared rollback itself fails, including the next restore point or human/external escalation path.
12. **Integrity reference** — a digest/signature/reference sufficient to detect that the rescue package or critical backup has changed unexpectedly when the Host makes this practical.

The rescue contract should favor concrete paths, commands, identifiers, conditions, and references over explanatory prose.

## Make rollback safe under two rescuers

The independent timer and the A2A rescue Agent may attempt recovery at nearly the same time.

Where the Host allows, make rollback idempotent or protect it with an atomic status/lock check so that:

- a second rollback does not corrupt an already-restored state;
- the rescue Agent can tell whether the timer already restored the change;
- successful restoration updates the package status in one place;
- cancelling or completing one recovery path does not leave the other path with stale assumptions.

Do not make successful recovery depend on the changed Agent being healthy enough to coordinate this race.

## Full change record

`change.md` should record:

- package creation time and canonical timezone;
- canonical language;
- what will change;
- why the change is being made;
- the exact components or paths affected;
- where the previous working state was preserved;
- how to reverse the change;
- the independent automatic rollback mechanism and its deadline;
- which other Agent received the recovery information;
- the current package status.

Write the human-readable parts of `change.md`, A2A recovery information, and rescue instructions in the canonical language. Keep commands, code, paths, identifiers, protocol fields, and other machine-sensitive content unchanged from the form required by the underlying system.

Use Host-native rollback commands or mechanisms when they are more reliable than a standalone script.

## Before applying the change

1. create the package;
2. preserve the previous working state of the affected part;
3. prepare and verify the rollback method;
4. prepare `rescue.yaml` with the executable recovery path, authorization conditions, and recovery scope;
5. arm an independent automatic rollback, normally 5–10 minutes later;
6. send the rescue contract and required recovery references to another Agent through A2A in the canonical language;
7. confirm that the other Agent received it;
8. only then apply the change.

The automatic rollback must not depend on the changed Agent remaining healthy.

## After applying the change

Confirm a normal bidirectional conversation with a human or another Agent.

If communication is normal, cancel the pending automatic rollback and mark the package as retained.

If the Agent becomes unreachable, leave the automatic rollback armed. If automatic recovery also fails, the other Agent should already have the rescue contract and recovery materials needed to restore the affected components without first reconstructing the change.

## Keep the package after completion

Do not discard the package after a successful change. Keep it as a durable history of what changed, when it changed, and how it can be reversed or understood later.
