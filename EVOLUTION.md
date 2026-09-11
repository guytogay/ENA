# Evolution

The Agent improves over time through one loop:

```text
experience
→ sleep: consolidate memory
→ dream: generate new possibilities
→ candidate
→ reality check / bounded trial
→ retain / revise / reject / restore
→ outcome becomes new experience
```

`SLEEP-DREAM.md` defines the Sleep and Dream steps. This file defines what happens to a candidate after it exists.

## 1. Preserve the candidate

A candidate may come from normal work, memory consolidation, dreaming, another Agent or the user.

Record only what is needed to test it:

- what is expected to improve;
- the proposed change;
- where the idea came from;
- what observable result would count as improvement;
- an important regression that must not occur;
- what live components or durable memories would change.

Use the timezone/language from `ENA.yaml`.

Example:

```text
~/.ena/evolution/candidates/
  20260912T020000+0800__improve-a2a-reconnect/
    candidate.yaml
```

See `examples/evolution/CANDIDATE.example.yaml`.

## 2. Capture the relevant baseline

Before changing anything, preserve the smallest real baseline that will later show whether the candidate helped.

Examples:

- the task/failure the change is meant to improve;
- current output from a repeatable check;
- an operational metric;
- current observed behavior;
- current retrieval/memory behavior.

Do not create a broad benchmark when a small direct comparison is enough.

## 3. Protect risky self-change

If the trial modifies code, runtime dependencies, services, communication, tool access, startup/recovery configuration or another critical operating component, use `SAFE-CHANGE.md`.

Link the candidate to the exact change package used for the trial.

For ordinary memory edits, use the memory system's own reversible/versioned path when sufficient. If the memory controls startup, recovery, communication or tool access, treat it as a critical self-change.

## 4. Separate survival from improvement

First confirm that the Agent remains reachable/recoverable.

Then ask whether the change actually improved the intended outcome.

A successful restart or successful conversation proves that the change did not kill the communication path. It does not prove the change was useful.

## 5. Observe real results

Compare the result with the baseline using evidence appropriate to the candidate:

- a real task;
- repeatable check;
- operational metric;
- before/after output;
- user feedback from actual use;
- retrieval/memory behavior;
- a period of normal operation without the targeted failure.

Record actual evidence, not only the Agent's interpretation.

## 6. Decide what survives

Use one practical outcome:

```text
retain   keep the change
revise   keep the idea, try another bounded variation
reject   current evidence does not justify it
restore  return to the previous behavior/state because the change regressed
```

If a safe-change package is still active, use its prepared rollback.

If a change was already retained and later needs reversal, make the reversal a new safe change against the current live state. Do not blindly run an old rollback after unrelated valid changes may have accumulated.

## 7. Feed the result back into memory

Preserve:

- what was tried;
- what happened;
- the final outcome;
- which assumptions changed;
- useful procedures/boundaries/uncertainties;
- negative and null results that should prevent repeated waste.

Later Sleep runs consolidate what reality established. Later Dream runs may reuse rejected ideas when new context makes a different variation plausible.

## 8. Keep history

A simple layout is:

```text
~/.ena/evolution/
  experience/
  candidates/
  retained/
  rejected/
  runs/
```

Indexes may point to stable candidate records instead of moving files. Keep links to safe-change packages rather than duplicating their backups and rollback material.
