# ENA Evolution

Status: working draft — not Current.

ENA evolution turns a useful improvement idea into a change that can be tried, observed, retained, revised, or rolled back without bypassing the Agent's recovery path.

## Start from a candidate, not a conclusion

When the Agent identifies a possible self-improvement, preserve it as a candidate before changing the live Agent.

Use the canonical timezone and language from `ENA.yaml`. Name candidate records with the same second-precise timestamp convention used by ACMS so their chronology remains clear.

Example:

```text
~/.ena/evolution/candidates/
  20260910T022500+0800__improve-a2a-reconnect/
    candidate.yaml
```

A candidate should state only what is needed to run the trial:

- what capability or behavior is expected to improve;
- what concrete change is proposed;
- what observable result would indicate improvement;
- what important regression must not occur;
- which live components the trial would modify.

The Agent may use its normal reasoning to decide whether a candidate is worth trying. ENA provides the durable execution path.

## Capture the relevant baseline before changing anything

Before the trial, preserve the smallest real baseline that will later let the Agent tell whether the candidate helped.

The baseline should be tied to the candidate's claimed improvement. Examples include:

- the real task or failure the change is intended to improve;
- current output from a repeatable check;
- the current operational metric;
- the current behavior observed by the user;
- the current frequency or conditions of the targeted failure.

Do not create a broad benchmark merely because evolution is occurring. Preserve only the evidence needed to compare this candidate before and after.

Record where the baseline evidence lives and when it was captured.

## Every body-affecting trial uses ACMS

If the candidate changes code, configuration, runtime dependencies, services, tools, communication paths, persistent operating rules, or another component that can affect the Agent's ability to operate or recover, run the trial through ACMS.

Do not create a separate evolution-specific mutation path.

Link the evolution candidate to the exact ACMS change package used for the trial. The ACMS package provides:

- preserved known-good state;
- executable rollback;
- independent timed recovery;
- A2A rescue information;
- exact change history.

## Separate survival from improvement

After applying the trial, first let ACMS determine whether the Agent remains reachable and recoverable.

Only after the protected change is safely retained long enough to observe should the evolution record decide whether the candidate actually improved anything.

A successful deployment or successful bidirectional conversation proves that the Agent survived the mutation. It does not prove the candidate was useful.

## Observe the result in real work

Evaluate the candidate against the baseline and the evidence appropriate to the intended improvement.

Use the smallest evidence that can distinguish useful change from no improvement or regression. Depending on the candidate, this may be:

- a real task that previously failed;
- a repeatable check or benchmark;
- an operational metric;
- a comparison of before/after outputs;
- user feedback from actual use;
- a period of normal operation without the targeted failure.

Record the actual post-change evidence rather than only the Agent's interpretation of it.

## Decide what survives

A trial should end in one of four practical outcomes:

- **retain** — the change is useful enough to remain the working state;
- **revise** — the candidate remains worth pursuing, but a different bounded change is needed;
- **reject** — the candidate did not justify another trial on current evidence;
- **restore** — return to the previous known-good state because the change caused regression or failed.

Record the evidence and outcome in the canonical timezone and language.

If evolution concludes that an already-survivable change should be undone, perform that restoration through the relevant ACMS recovery path rather than editing history by hand.

## Retained changes become the new starting point

When a trial is retained:

1. keep the linked ACMS package in `retained` state;
2. update `BODY.yaml` or `ENA.yaml` if a stable body location, capability, communication path, or recovery mechanism actually changed;
3. preserve the baseline, post-change evidence, and retention reason;
4. treat the retained live state as the starting point for later candidates.

Do not erase the previous package merely because the change succeeded. Later troubleshooting may need to know what changed and why it was kept.

## Failed ideas remain useful history

When a candidate is rejected or restored, preserve enough information to avoid repeating the same failed trial without new evidence.

At minimum record:

- the candidate;
- the baseline;
- the ACMS package used, if any;
- what happened;
- the observed result;
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

A candidate folder may move or be indexed into `retained/` or `rejected/` after adjudication. Keep links to corresponding ACMS packages rather than duplicating backups and rollback material.

A minimal machine-readable candidate record is shown in [`examples/evolution/CANDIDATE.example.yaml`](examples/evolution/CANDIDATE.example.yaml).

## The loop

```text
notice an improvement opportunity
        ↓
preserve candidate + relevant baseline
        ↓
choose a bounded trial
        ↓
apply through ACMS when the body is affected
        ↓
prove the Agent survived the mutation
        ↓
observe the intended effect against baseline
        ↓
retain / revise / reject / restore
        ↓
preserve the result for the next cycle
```
