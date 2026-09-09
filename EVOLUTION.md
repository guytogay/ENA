# ENA Evolution

Status: working draft — not Current.

ENA evolution should help an Agent become better over time by changing what it retains, generating new possibilities from what it has experienced, and selecting useful changes against reality.

A practical loop has three connected processes:

```text
experience / existing memory
        ↓
memory consolidation
        ↓
stronger, cleaner, better-connected retained knowledge and adaptations
        ↓
recombination / dreaming
        ↓
new associations, hypotheses, and candidate variations
        ↓
reality contact / bounded trial
        ↓
retain / revise / reject / restore
        ↓
feed the result back into memory
```

The concrete implementation may use Host-native memory, schedulers, repositories, databases, model memory facilities, or other available mechanisms.

## 1. Consolidate memory

Evolution is not only changing code or configuration. The Agent should periodically improve the memory substrate that shapes future work.

During an idle, scheduled, or otherwise suitable consolidation cycle, inspect relevant accumulated experience and memory for things such as:

- repeated successes or failures;
- repeated user corrections;
- duplicate or fragmented knowledge;
- contradictions;
- stale or superseded information;
- useful procedures that recur across tasks;
- important boundaries or exceptions;
- unresolved questions or loops;
- surprising outcomes;
- associations that have become stronger across multiple experiences.

Possible consolidation actions include:

- merge duplicate memories;
- connect related memories that were previously isolated;
- turn repeated experience into reusable procedural knowledge;
- strengthen useful cues or associations;
- narrow an overgeneralized lesson;
- preserve counterexamples and uncertainty;
- mark stale material dormant or superseded;
- prune material that no longer earns active retrieval cost;
- create a candidate improvement when experience suggests the Agent itself should change.

Keep occurrence/provenance records where they remain useful. Do not silently rewrite history merely to make the current memory cleaner.

When consolidation rewrites or removes durable memory, use the memory system's versioning/history/backup capability where available so a destructive consolidation mistake can be reversed.

The result of consolidation should be a memory system that makes useful knowledge, procedures, associations, and learned sensitivities easier to express in future work — not merely a longer summary document.

## 2. Dream / recombine

The Agent should also have a low-risk way to produce variation from material it already knows.

A dreaming cycle may deliberately sample and recombine memory fragments that are not normally adjacent:

```text
memory A
+
memory B
+
memory C
        ↓
new association / hypothetical scenario / possible mechanism
        ↓
candidate variation
```

Useful operations may include:

- connect experiences from different tasks or domains;
- vary assumptions or ordering;
- combine partial solutions;
- ask what two distant observations have in common;
- imagine a failure or success under a changed environment;
- derive several competing explanations rather than one;
- use unresolved contradictions as material for new hypotheses.

Dream output is speculative material, not factual memory.

Do not automatically promote a generated association, imagined event, or hypothetical explanation into observed truth. Preserve provenance so later work can distinguish:

- observed experience;
- remembered fact/knowledge;
- generated association;
- candidate hypothesis;
- selected adaptation.

The useful output of dreaming is the new search/variation space it creates. A polished dream narrative is optional.

## 3. Preserve candidates

When consolidation, dreaming, normal work, another Agent, or the user produces a possible self-improvement, preserve it as a candidate before changing the live Agent.

Use the canonical timezone and language from `ENA.yaml`. Name durable candidate records with the same second-precise timestamp convention used by ACMS.

Example:

```text
~/.ena/evolution/candidates/
  20260910T022500+0800__improve-a2a-reconnect/
    candidate.yaml
```

A candidate should state only what is needed to evaluate it:

- what capability, behavior, memory, or procedure is expected to improve;
- what concrete change is proposed;
- where the candidate came from: experience, consolidation, dreaming, external contribution, or another source;
- what observable result would indicate improvement;
- what important regression must not occur;
- which live components or durable memories the trial would modify.

## 4. Capture the relevant baseline before changing anything

Before a trial, preserve the smallest real baseline that will later let the Agent tell whether the candidate helped.

The baseline should be tied to the claimed improvement. Examples include:

- the real task or failure the change is intended to improve;
- current output from a repeatable check;
- the current operational metric;
- the current behavior observed by the user;
- the current frequency or conditions of the targeted failure;
- the current memory/retrieval behavior when the candidate concerns memory.

Do not create a broad benchmark merely because evolution is occurring. Preserve only the evidence needed to compare this candidate before and after.

## 5. Protect body-affecting trials with ACMS

If a candidate changes code, configuration, runtime dependencies, services, tools, communication paths, persistent operating rules, or another component that can affect the Agent's ability to operate or recover, run the trial through [`ACMS.md`](ACMS.md).

Do not create a separate evolution-specific body mutation path.

Link the evolution candidate to the exact ACMS package used for the trial.

Memory-only changes may use the memory system's own reversible/versioned change path when they do not affect the Agent's survivability surface. If a memory or persistent rule controls startup, recovery, communication, tool access, or another body-critical path, protect the consequential change accordingly.

## 6. Separate survival from improvement

After a body-affecting trial, first confirm through ACMS that the Agent remains reachable and recoverable.

Only then determine whether the candidate actually improved anything.

A successful deployment or successful conversation proves survival of the mutation. It does not prove useful evolution.

## 7. Observe the result in real work

Evaluate the candidate against the baseline and the evidence appropriate to the intended improvement.

Use the smallest evidence that can distinguish useful change from no improvement or regression. Depending on the candidate, this may be:

- a real task that previously failed;
- a repeatable check or benchmark;
- an operational metric;
- a comparison of before/after outputs;
- user feedback from actual use;
- improved retrieval or memory application;
- a period of normal operation without the targeted failure.

Record actual post-change evidence rather than only the Agent's interpretation of it.

## 8. Decide what survives

A candidate should end in one of four practical outcomes:

- **retain** — the change is useful enough to remain;
- **revise** — the idea remains promising but needs another bounded variation;
- **reject** — current evidence does not justify continuing it;
- **restore** — return to the previous behavior/state because the change caused regression or failed.

A rejected candidate may still remain useful material for future dreaming when new evidence or a changed environment makes a different variation plausible.

### Restore safely

If the original ACMS package is still active in `applied`/recovery state, use that package's prepared rollback.

If the original change has already reached ACMS `retained`, do not blindly execute its old rollback later. Other valid changes may have accumulated on top of it. Create a new ACMS-protected reversal change that references the original package and reverses only the intended parts against the current live state.

## 9. Feed selected experience back into memory

After selection, update the Agent's durable memory with what reality established:

- what was tried;
- what happened;
- what was retained, revised, rejected, or restored;
- which assumptions changed;
- what new procedure, association, boundary, or uncertainty should survive;
- what should become material for later consolidation or dreaming.

Do not retain only successful changes. Negative results reduce repeated waste and provide variation boundaries for future work.

## 10. Keep evolution history

A simple layout under the ENA home can be:

```text
~/.ena/
  evolution/
    candidates/
    retained/
    rejected/
```

Keep each candidate's durable record at a stable path. `retained/` and `rejected/` may be indexes/references rather than moving the original record, so links do not break.

Keep links to corresponding ACMS packages rather than duplicating backups and rollback material.

A minimal machine-readable candidate record is shown in [`examples/evolution/CANDIDATE.example.yaml`](examples/evolution/CANDIDATE.example.yaml).
