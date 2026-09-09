# ENA Evolution

Status: working draft — not Current.

ENA evolution turns a useful improvement idea into a change that can be tried, observed, retained, revised, or rolled back without bypassing the Agent's recovery path.

## Start from a candidate, not a conclusion

When the Agent identifies a possible self-improvement, preserve it as a candidate before changing the live Agent.

A candidate should state only what is needed to run the trial:

- what capability or behavior is expected to improve;
- what concrete change is proposed;
- what observable result would indicate improvement;
- what important regression must not occur;
- which live components the trial would modify.

The Agent may use its normal reasoning to decide whether a candidate is worth trying. ENA provides the durable execution path.

## Every body-affecting trial uses ACMS

If the candidate changes code, configuration, runtime dependencies, services, tools, communication paths, persistent operating rules, or another component that can affect the Agent's ability to operate or recover, run the trial through ACMS.

Do not create a separate evolution-specific mutation path.

The ACMS package for the trial provides:

- preserved known-good state;
- executable rollback;
- independent timed recovery;
- A2A rescue information;
- exact change history.

## Observe the result in real work

After the change remains reachable, evaluate the candidate against the evidence appropriate to that improvement.

Use the smallest evidence that can distinguish useful change from no improvement or regression. Depending on the candidate, this may be:

- a real task that previously failed;
- a repeatable check or benchmark;
- an operational metric;
- a comparison of before/after outputs;
- user feedback from actual use;
- a period of normal operation without the targeted failure.

Do not keep a change merely because it deployed successfully. Deployment proves survivability, not improvement.

## Decide what survives

A trial should end in one of four practical outcomes:

- **retain** — the change is useful enough to become the new working state;
- **revise** — keep the candidate alive, but prepare a different bounded change;
- **reject** — the candidate did not earn another trial;
- **restore** — return to the previous known-good state because the change caused regression or failed.

Record the actual evidence and outcome in the canonical timezone and language.

## Retained changes become the new starting point

When a trial is retained:

1. mark the ACMS change package `retained`;
2. update any affected ENA body/configuration references if their stable location or recovery path changed;
3. preserve the evidence that justified retention;
4. treat the retained state as the current starting point for later changes.

Do not erase the previous package merely because the change succeeded. Later troubleshooting may need to know what changed and why it was kept.

## Failed ideas remain useful history

When a candidate is rejected or restored, preserve enough information to avoid repeating the same failed experiment without new evidence.

At minimum record:

- the candidate;
- the change package used;
- what happened;
- why it was rejected/restored;
- what new condition would justify revisiting it, if any.

## Evolution records

A simple layout under the ENA home can be:

```text
~/.ena/
  evolution/
    candidates/
    retained/
    rejected/
```

Use another Host-appropriate structure if it is more reliable. Keep links from evolution records to the corresponding ACMS packages rather than duplicating backups and rollback material.

## The loop

```text
notice an improvement opportunity
        ↓
preserve a candidate
        ↓
choose a bounded trial
        ↓
apply through ACMS when the body is affected
        ↓
prove the Agent is still reachable
        ↓
observe the intended effect in reality
        ↓
retain / revise / reject / restore
        ↓
preserve the result for the next cycle
```
