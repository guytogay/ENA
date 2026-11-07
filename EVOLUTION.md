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

Improvement may mean **removing, merging, simplifying or retiring** a costly step, instruction, memory, tool or workflow, not adding another one. Start from the most consequential observed friction or opportunity in the current situation; inherited procedures are hypotheses about what helps, not evidence that they still help. This is a choice of focus, not a required analysis ritual.

When self-maintenance is authorized by the owner or trusted Host policy, the Agent may **choose which capability to develop, adapt or retire** without asking for a new prompt for each idea. Choose for the actual Host, user benefit and observed leverage, including unexpected cross-domain possibilities; choose no change when nothing earns its cost. Autonomy to select a candidate does not grant permission to install tools, expand access or alter critical state.

A **peer process review** is one optional way to notice a candidate: a peer can inspect an authorized, bounded task trace and suggest a smaller or better execution path. Keep the trace and the peer's opinion as separate evidence. The suggestion remains speculative until a later real task or bounded comparison supports it; agreement between Agents is not proof of improvement. Do not start peer reviews automatically for every task. If the user explicitly ends or cancels the task, stop its coding, research, review and exchange work immediately rather than completing a planned loop. Only minimal cleanup needed to contain a side effect already in progress may continue, and it should be reported.

Before reality contact, keep it under:

```text
~/.ena/evolution/candidates/speculative/
```

Dream-generated candidates always start with:

```json
{
  "truth_status": "speculative"
}
```

Record only what is needed to test the candidate:

- expected improvement;
- proposed bounded change;
- origin/source references;
- observable result that would count as improvement;
- important regression that must not occur;
- components or durable memories that would change;
- any tool/skill/connector/API that must be installed, enabled or authorized first.

`tools/candidate_record.py` provides a reference writer for initial speculative candidates. It writes JSON artifacts; `examples/evolution/CANDIDATE.example.json` shows the machine artifact shape emitted by that tool.

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

## 5. Validate close to the changed state

When the Host provides a deterministic check for the property being changed, run it as close to the corresponding mutation as practical rather than only at the end of the whole trial.

Examples include parser/schema checks, compilation, type checking, targeted tests, build checks, health probes, access checks and retrieval/readability checks.

A failed check is useful evolution evidence when the repair path is preserved: `SAFE-CHANGE.md` owns the linked `FAIL -> repair -> PASS` shape and the `tools/validate_change.py` wrapper that records it, which Host-native hooks may also implement.

Incremental validation does not prove the candidate improved the intended outcome. It prevents obvious defects from surviving too long and creates better evidence about how the candidate behaved.

## 6. Separate survival from improvement

First confirm the Agent remains usable/recoverable. Then ask whether the change actually improved the intended outcome.

A successful restart, new session, passing syntax check, or successful conversation proves only the property it directly checks. It does not by itself prove the candidate was useful.

## 7. Observe real results

Compare the result with the baseline using evidence appropriate to the candidate:

- a real task;
- repeatable check;
- operational metric;
- before/after output;
- user feedback from actual use;
- retrieval/memory behavior;
- deterministic validation and repair history;
- a period of normal operation without the targeted failure.

Record actual evidence, including negative and null results. Compare user-visible benefit against **total** extra cost: elapsed time, model/tool usage, review overhead, maintenance and regressions. A cleaner internal process that makes the real task worse is not an improvement.

## 8. Decide what survives

Use one practical outcome:

```text
retain   evidence supports keeping the change
revise   idea remains useful but needs another bounded variation
reject   current evidence does not justify it
restore  return to the previous state because the trial regressed
```

The surrounding Agent/user/Host makes this judgment. The reference tool does not decide whether evidence is sufficient. `tools/candidate_outcome.py` only persists an outcome that has already been decided, together with explicit evidence references and any residual boundary.

For a speculative artifact that has completed reality contact:

```text
python tools/candidate_outcome.py SPECULATIVE_CANDIDATE \
  --outcome retain|revise|reject|restore \
  --evidence REAL_TRIAL_OR_VALIDATION_REFERENCE \
  --decided-by REAL_DECISION_ACTOR_OR_WORKFLOW
```

The source speculative artifact remains immutable occurrence history. The decision record carries its reference + digest and a compact snapshot of the candidate/provenance. One speculative candidate receives one recorded outcome: a revised idea should become a new candidate, and a later reversal of a retained production change is new change/experience evidence rather than a second decision on the old speculative artifact.

A retained candidate is recorded under:

```text
~/.ena/evolution/candidates/selected/
```

with the evidence and outcome that justified selection. `revise`, `reject`, and `restore` are still durable evidence, but they are recorded under:

```text
~/.ena/evolution/candidates/outcomes/
```

so negative/null results do not disappear merely because they were not selected.

**Selected does not necessarily mean already in production.**

- If the bounded trial happened directly on live state and the change is retained, production application may already be complete.
- If the trial happened in a sandbox, branch, worktree, preview environment or other isolated copy, apply the selected change to live state separately.
- Use `SAFE-CHANGE.md` when production application can affect critical runtime state.
- Re-verify required capabilities and permissions at production time.
- Re-run relevant deterministic checks near the production change and observe the live result afterward; sandbox success is not proof of production success.

Selection also does not automatically make generated prose factual memory. Later Sleep decides how verified experience changes durable memory.

If a retained production change later needs reversal, make that reversal against the current live state rather than blindly running an old rollback after unrelated valid changes may have accumulated.

## 9. Feed the result back into experience

Preserve what was tried, where it was tried, whether it reached production, what happened afterward, the final outcome, changed assumptions, useful procedures/boundaries/uncertainties, and negative/null results that should prevent repeated waste.

Also preserve useful validation/repair trajectories. Repeated evidence that the same structural mistake triggers the same deterministic failure and repair may later become a stronger procedure, retrieval cue or preventive check during Sleep.

When judging an improvement, observe the **whole Host-visible task path**, including foreground interaction, background execution, peer work, session continuity and recovery. Optimizing one layer is not progress if the end-to-end result deteriorates. A Host may use event/hook-driven task progression to release ready work without a timed gap; that general project orchestration belongs in the Host or a separate work tool, not in ENA's candidate records. Failure detection, Agent activation and returning to the same messaging channel require real Host integration; ENA cannot supply them by instruction alone. The trigger/recovery path itself may become a bounded evolution candidate when observed failures justify it; the Agent must still test the change and avoid self-perpetuating retries.

Later Sleep consolidates what reality established. Later Dream runs may reuse rejected ideas when new context supports a different variation.

## 10. Keep the history simple

A minimal layout is:

```text
~/.ena/evolution/
  experience/
  candidates/
    speculative/
    selected/
    outcomes/
  runs/
```

Keep stable links to recovery packages rather than duplicating their backups and rollback material.
