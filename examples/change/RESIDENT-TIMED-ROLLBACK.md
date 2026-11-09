# Resident-runtime timed rollback

This is a concrete Host-wiring example for [SAFE-CHANGE](../../SAFE-CHANGE.md) and [brick 35](../../BRICKS.md). It preserves the owner's simple rule:

> Before a consequential resident-runtime self-change, start an independent 5–10 minute rollback clock. Cancel it only after a normal two-way exchange proves the changed Agent is reachable. If no confirmation arrives, restore the previous working state automatically.

This is a Host adapter recipe, **not a universal ENA daemon**. The ENA reference tools record the change package and state; they do not create, start, cancel, or supervise a timer. The Host must wire the actual mutation boundary to the timer and recovery executor.

## When to use it

Use this for a resident Agent (service, daemon, long-running container, VM Agent or always-on worker) when a change could prevent it from:

- starting after restart;
- communicating with a human or reachable peer;
- using tools required to receive repair instructions;
- reaching or executing its own recovery path.

A 5–10 minute window is a starting point, not a universal constant. Allow enough time for the real service startup and one external exchange. Do not apply this daemon pattern to a session/coding Agent; use its durable Git/worktree and new-session recovery path instead.

## Required pieces

Prepare these before the first live write:

1. **Known-good state:** an exact backup, revision or snapshot outside the component being changed. Record its identity/hash and the exact restore scope.
2. **Host-owned timer:** a scheduler/supervisor that continues if the Agent process exits. Verify that the timer is active before allowing the change.
3. **Independent rollback executor:** a Host-managed command that can stop the target, restore only the declared scope, restart it and record the result. It must not call an LLM, depend on the changed Agent, or read instructions from the failed Agent's conversation.
4. **External confirmation path:** a human or reachable peer Agent can complete a normal two-way exchange with the changed Agent and cause the Host to cancel this specific change's timer. A2A is useful when present, but a human path remains valid.
5. **Per-change serialization:** apply, confirmation and rollback use one lock or equivalent atomic compare-and-swap on the change ID/state. A timer from an older change must never undo a later retained change.

The rollback executor should be preinstalled or otherwise available outside the changed tree. Do not make the Agent's only copy of the recovery command part of the mutation.

## State and ordering

Use the SAFE-CHANGE package as the durable record:

~~~text
preparing
  -> armed       known-good state and external timer are ready; no live write has begun
  -> applied     immediately before the first live write; the change may now be in flight
  -> retained    an external two-way liveness exchange succeeded; keep the new state

timeout:
  armed          -> cancelled   no live write began; refuse any later apply
  applied        -> restoring   stop any still-running writer, then restore the declared scope
  restoring      -> restored    previous state is back and recovery checks pass
  restoring      -> failed      restore/restart/verification did not recover usability
~~~

The Host adapter must make the boundary race-safe:

- The apply path checks that the timer is still active, obtains the per-change lock, records applied immediately before the first live write, and performs the bounded mutation.
- The timer path obtains the same lock. If it wins while state is still armed, it records cancelled; the apply path must then refuse to proceed. If state is applied, it stops any still-running writer before restoring.
- If a writer can hang while holding the lock, the Host supervisor needs a bounded way to stop that writer and release the lock. Never let the timer wait forever or restore concurrently with live writes.
- The external confirmation path obtains the same lock. It may move applied to retained and cancel the timer only after the external exchange has actually completed. If rollback has already claimed the change, confirmation must refuse.
- The rollback path is idempotent. retained, cancelled, restored and failed are terminal for that change ID; duplicate timer delivery must not repeat destructive work.

The confirmation proves **liveness**, not perfect health. A normal human↔Agent or peer-Agent↔Agent exchange is enough to show that the Agent can receive repair instructions. Record a small deterministic check of the changed function when one is available, but do not turn this into a requirement to prove every capability healthy before cancelling the only rescue window.

The changed Agent's own text saying "I'm healthy" is not independent confirmation. The human or peer must have received a normal reply through a path that the change did not break. The Host integration—not the Agent's self-report—performs the cancellation.

## systemd example

Use a Host-managed system service identity with only the permissions needed to restore the declared files and restart the target service. Do not give an Agent unrestricted root merely to make the example work. If using a user manager, verify that it remains running independently (for example, configure and test linger); do not assume an interactive login keeps it alive.

### Transient timer: protects against Agent/service-process failure

For a Host where only the Agent process/service restart is in scope:

~~~bash
systemd-run \
  --unit=ena-rollback-change-id-001 \
  --on-active=10m \
  --timer-property=AccuracySec=1s \
  /usr/local/libexec/ena-rollback change-id-001

systemctl is-active --quiet ena-rollback-change-id-001.timer
~~~

The path /usr/local/libexec/ena-rollback is a **Host-provided** executor, not a shipped ENA command. It must implement the state/lock/restore/restart/verification contract above. The timer is managed by systemd rather than by the Agent process, so an Agent service restart does not stop the countdown.

This systemd-run timer is transient. It is **not** a host-reboot-persistent installation: if the whole operating system reboots, the transient unit itself is not recreated. Do not claim protection against host reboot from this command alone.

### Persistent timer: include host reboot in the failure model

If the operating system itself may reboot during the rollback window, persist a per-change timer unit and its service outside the Agent's files. For example, install a service template:

~~~ini
# /etc/systemd/system/ena-rollback@.service
[Unit]
Description=ENA rollback for change %i

[Service]
Type=oneshot
ExecStart=/usr/local/libexec/ena-rollback %i
~~~

Create a one-shot timer file for this exact change ID and absolute UTC deadline:

~~~ini
# /etc/systemd/system/ena-rollback-change-id-001.timer
[Unit]
Description=ENA rollback deadline for change-id-001

[Timer]
OnCalendar=2026-11-09 03:25:00 UTC
Persistent=true
AccuracySec=1s
Unit=ena-rollback@change-id-001.service

[Install]
WantedBy=timers.target
~~~

Then install and verify it before applying the change:

~~~bash
systemctl daemon-reload
systemctl enable --now ena-rollback-change-id-001.timer
systemctl is-active --quiet ena-rollback-change-id-001.timer
systemctl list-timers --all ena-rollback-change-id-001.timer
~~~

Replace the example deadline with the actual deadline calculated from the Host's clock. Validate the calendar expression and clock before relying on it. Persistent=true catches a missed calendar event when the timer is activated after the machine was powered down; it applies to OnCalendar timers, not monotonic OnActiveSec timers. The timer unit must itself be installed/enabled persistently for this to help after reboot.

After external confirmation, the Host confirmation adapter should atomically mark the change retained under the same lock, then stop/disable that timer:

~~~bash
systemctl disable --now ena-rollback-change-id-001.timer
~~~

The Host may then remove the per-change timer file and run systemctl daemon-reload. If expiry has already started the rollback service, the shared state/lock decides the winner; stopping the timer alone is not proof that an already-triggered rollback service has stopped.

See the official [systemd-run documentation](https://www.freedesktop.org/software/systemd/man/latest/systemd-run.html) and [systemd.timer documentation](https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html) for the exact timer semantics and options.

## External confirmation interface

The following is an **interface shape**, not a command shipped by ENA:

~~~text
ena-host-confirm CHANGE_ID --receipt EXTERNAL_EXCHANGE_RECEIPT
~~~

The Host should accept it only from an authorized human or peer integration, for the exact pending change ID, after it has observed a completed two-way exchange. Use a one-time receipt/nonce or equivalent replay protection. Do not expose an unauthenticated network endpoint that lets arbitrary callers cancel rollback.

A human may confirm after receiving a normal reply in the usual channel. A peer Agent may confirm after sending a challenge and receiving a normal response over A2A. If neither can confirm before the deadline, the timer fires; the timeout path does not wait for either of them.

## Rollback executor contract

On expiry, the Host executor should:

1. claim the change ID under the per-change lock;
2. refuse destructive action if the state is already terminal;
3. if state is armed, mark the unapplied change cancelled and prevent a late apply;
4. if state is applied, stop the target/writer, restore only restore_only from known_good, and restart using the recorded Host action;
5. compare restored bytes/revision with the recorded known-good identity;
6. run the smallest independent startup/health check and record whether communication returned;
7. write restored or failed with durable evidence; if failed, notify the available rescuer without entering an infinite retry/restart loop.

No LLM or human is part of steps 1–7. A rescuer may inspect a failed result later, but the Agent does not need to be alive for rollback to happen.

## Minimum fault-injection drill

Do not call the mechanism verified because the timer appears in list-timers. Exercise the whole path on an isolated probe first:

| Trial | Required observation |
|---|---|
| Normal restart + external exchange | Human/peer receives a normal reply; confirmation cancels the timer; no rollback occurs |
| Agent process killed after apply | Timer still fires; previous bytes/revision are restored; service restarts |
| Invalid startup/communication config | Target cannot participate; timeout executor restores the known-good state without LLM/human action |
| Timer and confirmation race | Exactly one wins; no later timer can undo a retained change |
| Duplicate timer delivery | Second invocation is a safe no-op |
| Host reboot before deadline (if in scope) | Persistent timer catches up after boot and runs the pending rollback |
| Rollback itself fails | State becomes failed, evidence remains, and no endless retry loop starts |

Record the Host/runtime, timer type, exact changed scope, known-good hash/revision, deadline, timer/executor identity, raw timestamps, restored hash/revision, restart result and independent health/communication evidence.

A successful drill on one Host establishes that Host path only. It does not prove every systemd version, container platform, cron installation or Agent framework has the same behavior.
