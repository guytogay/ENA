# ACMS v0.1

Status: working draft — not Current.

Use ACMS for changes that can affect the Agent's ability to keep operating, communicate, or repair itself.

## One change, one package

Create one independent package for each change before applying it.

Use a UTC timestamp precise to the second in the folder name so packages sort naturally and remain unambiguous across Hosts and Agents.

Example:

```text
changes/
  20260909T170637Z__fix-agent-channel/
```

If more than one package may be created in the same second, append a short unique ID:

```text
changes/
  20260909T170637Z__a4f2__fix-agent-channel/
```

## Package contents

Each package should contain enough information and material to reverse the change without first having to investigate what happened.

A minimal package can contain:

```text
change.md
backup/
rollback.sh | rollback.ps1 | equivalent Host-native rollback
status
```

`change.md` should record:

- package creation time, including timezone;
- what will change;
- why the change is being made;
- the exact components or paths affected;
- where the previous working state was preserved;
- how to reverse the change;
- the independent automatic rollback mechanism and its deadline;
- which other Agent received the recovery information;
- the current package status.

Use Host-native rollback commands or mechanisms when they are more reliable than a standalone script.

## Before applying the change

1. create the package;
2. preserve the previous working state of the affected part;
3. prepare and verify the rollback method;
4. arm an independent automatic rollback, normally 5–10 minutes later;
5. send the recovery information to another Agent through A2A;
6. confirm that the other Agent received it;
7. only then apply the change.

The automatic rollback must not depend on the changed Agent remaining healthy.

## After applying the change

Confirm a normal bidirectional conversation with a human or another Agent.

If communication is normal, cancel the pending automatic rollback and mark the package as retained.

If the Agent becomes unreachable, leave the automatic rollback armed. If automatic recovery also fails, the other Agent should already have the package information needed to restore the affected components.

## Keep the package after completion

Do not discard the package after a successful change. Keep it as a durable history of what changed, when it changed, and how it can be reversed or understood later.
