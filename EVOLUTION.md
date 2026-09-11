# Evolution

The Agent improves over time through one loop:

```text
experience
→ Sleep: consolidate memory
→ Dream or ordinary work: generate candidates
→ reality check / bounded trial
→ retain / revise / reject / restore
→ production application when needed
→ outcome becomes new experience
```

`SLEEP-DREAM.md` defines the experimental Sleep/Dream path. This file defines what happens after a candidate exists.

## 1. Preserve the candidate as a candidate

A candidate may come from normal work, memory consolidation, Dream, another Agent, the user, a knowledge source or a newly discovered capability.

Before reality contact, keep it under:

```text
~/.ena/evolution/candidates/speculative/
```

Dream-generated candidates always start with:

```yaml
truth_status: speculative
```

Record only what is needed to test the candidate:

- expected improvement;
- proposed bounded change;
- origin/source references;
- observable result that would count as improvement;
- important regression that must not occur;
- components or durable memories that would change;
- any tool/skill/connector/API that must be installed, enabled or authorized first.

`tools/candidate_record.py` provides a reference writer for initial speculative candidates.

## 2. Capture the relevant baseline

Before changing anything, preserve the smallest real baseline that can later show whether the candidate helped.

Examples include the targeted task/failure, repeatable check, operational metric, current observed behavior or current retrieval/memory behavior.

Do not create a broad benchmark when a small direct comparison is enough.

## 3. Verify required capabilities

If the candidate depends on a tool, skill, connector/plugin, API or other capability, verify the live state before relying on it:

- installed/enabled or only discoverable;
- current permissions/authorization;
- current interface/capabilities;
- any required user/operator approval.

A capability seen in a Dream, catalog or Agent Card is only a possibility until live verification succeeds.

## 4. Protect risky self-change

If the trial modifies code, runtime dependencies, services, communication, tool access, startup/recovery configuration or another critical operating component, use `SAFE-CHANGE.md` with the appropriate Host profile.

Link the candidate to the exact recovery package used for the trial.

For ordinary memory edits, use the memory system's own reversible/versioned path when sufficient. If memory controls startup, recovery, communication or tool access, treat it as critical runtime state.

## 5. Separate survival from improvement

First confirm the Agent remains usable/recoverable. Then ask whether the change actually improved the intended outcome.

A successful restart, new session or successful conversation proves recoverability/communication. It does not prove the candidate was useful.

## 6. Observe real results

Compare the result with the baseline using evidence appropriate to the candidate:

- a real task;
- repeatable check;
- operational metric;
- before/after output;
- user feedback from actual use;
- retrieval/memory behavior;
- a period of normal operation without the targeted failure.

Record actual evidence, including negative and null results.

## 7. Decide what survives

Use one practical outcome:

```text
retain   evidence supports keeping the change
revise   idea remains useful but needs another bounded variation
reject   current evidence does not justify it
restore  return to the previous state because the trial regressed
```

A candidate that survives reality contact may be recorded under:

```text
~/.ena/evolution/candidates/selected/
```

with the evidence and outcome that justified selection.

**Selected does not necessarily mean already in production.**

- If the bounded trial happened directly on live state and the change is retained, production application may already be complete.
- If the trial happened in a sandbox, branch, worktree, preview environment or other isolated copy, apply the selected change to live state separately.
- Use `SAFE-CHANGE.md` when production application can affect critical runtime state.
- Re-verify required capabilities and permissions at production time.
- Observe the live result after application; a sandbox success is not proof of production success.

Selection also does not automatically make generated prose factual memory. Later Sleep decides how verified experience changes durable memory.

If a retained production change later needs reversal, make that reversal against the current live state rather than blindly running an old rollback after unrelated valid changes may have accumulated.

## 8. Feed the result back into experience

Preserve what was tried, where it was tried, whether it reached production, what happened afterward, the final outcome, changed assumptions, useful procedures/boundaries/uncertainties, and negative/null results that should prevent repeated waste.

Later Sleep consolidates what reality established. Later Dream runs may reuse rejected ideas when new context supports a different variation.

## 9. Keep the history simple

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
