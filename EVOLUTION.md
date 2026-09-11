# Evolution

The Agent improves over time through one loop:

```text
experience
→ Sleep: consolidate memory
→ Dream or ordinary work: generate candidates
→ reality check / bounded trial
→ retain / revise / reject / restore
→ outcome becomes new experience
```

`SLEEP-DREAM.md` defines the experimental Sleep/Dream path. This file defines what happens after a candidate exists.

## 1. Preserve the candidate as a candidate

A candidate may come from normal work, memory consolidation, Dream, another Agent or the user.

Before reality contact, keep it under:

```text
~/.ena/evolution/candidates/speculative/
```

with a truth/status marker that makes its epistemic state explicit. Dream-generated candidates always start with:

```yaml
truth_status: speculative
```

Record only what is needed to test the candidate:

- expected improvement;
- proposed bounded change;
- origin/source references;
- observable result that would count as improvement;
- important regression that must not occur;
- components or durable memories that would change.

`tools/candidate_record.py` provides a reference writer for initial speculative candidates.

## 2. Capture the relevant baseline

Before changing anything, preserve the smallest real baseline that can later show whether the candidate helped.

Examples include the targeted task/failure, repeatable check, operational metric, current observed behavior or current retrieval/memory behavior.

Do not create a broad benchmark when a small direct comparison is enough.

## 3. Protect risky self-change

If the trial modifies code, runtime dependencies, services, communication, tool access, startup/recovery configuration or another critical operating component, use `SAFE-CHANGE.md` with the appropriate Host profile.

Link the candidate to the exact recovery package used for the trial.

For ordinary memory edits, use the memory system's own reversible/versioned path when sufficient. If memory controls startup, recovery, communication or tool access, treat it as critical runtime state.

## 4. Separate survival from improvement

First confirm the Agent remains usable/recoverable. Then ask whether the change actually improved the intended outcome.

A successful restart, new session or successful conversation proves recoverability/communication. It does not prove the candidate was useful.

## 5. Observe real results

Compare the result with the baseline using evidence appropriate to the candidate:

- a real task;
- repeatable check;
- operational metric;
- before/after output;
- user feedback from actual use;
- retrieval/memory behavior;
- a period of normal operation without the targeted failure.

Record actual evidence, including negative and null results.

## 6. Decide what survives

Use one practical outcome:

```text
retain   evidence supports keeping the change
revise   idea remains useful but needs another bounded variation
reject   current evidence does not justify it
restore  return to the previous state because the trial regressed
```

A candidate that survives reality contact may be copied/recorded under:

```text
~/.ena/evolution/candidates/selected/
```

with the evidence and outcome that justified selection. Selection still does not automatically make every generated sentence factual memory; later Sleep decides how verified experience changes durable memory.

If a safe-change package is still active, use its prepared rollback. If a change was already retained and later needs reversal, make that reversal a new safe change against the current live state rather than blindly running an old rollback.

## 7. Feed the result back into experience

Preserve what was tried, what happened, the final outcome, changed assumptions, useful procedures/boundaries/uncertainties, and negative/null results that should prevent repeated waste.

Later Sleep consolidates what reality established. Later Dream runs may reuse rejected ideas when new context supports a different variation.

## 8. Keep the history simple

A minimal layout is:

```text
~/.ena/evolution/
  experience/
  candidates/
    speculative/
    selected/
  runs/
```

Keep stable links to recovery packages rather than duplicating their backups and rollback material.
