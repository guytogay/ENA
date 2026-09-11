# Sleep / Dream Quickstart

Use this after minimum First Use is complete and the Agent has identified the memory sources needed for this experiment.

Current sampler sizes and weights are experimental starting parameters. Do not treat them as ENA rules.

## 1. Create the working directories

```text
~/.ena/evolution/
  experience/
  candidates/
    speculative/
    selected/
  runs/
    sleep/
    dream/
  locks/
```

Keep the real long-term memory where the Host already keeps it.

## 2. Create `sleep-dream.yaml`

Start from `examples/evolution/SLEEP-DREAM.example.yaml` and fill in the actual memory sources, write/update method, restore path, excluded sources, run limits and scheduler references when available.

## 3. Feed useful experience

Preserve concise records for corrections, repeated success/failure, surprising outcomes, unresolved problems, useful procedures or evolution results when the Host does not already keep equivalent durable records.

Do not dump whole conversations by default.

## 4. Run Sleep once manually

```text
lock memory scope
→ collect new experience and relevant memory
→ find duplication/conflict/staleness/overreach/procedures/boundaries/unresolved links
→ write a consolidation plan before changing memory
→ preserve a reversible pre-run state
→ apply only the plan
→ verify memory and provenance remain usable
→ record the run
→ unlock
```

If verification fails, restore the pre-run state. A prettier summary is not success unless later retrieval or behavior improves.

## 5. Run Dream once manually

Choose either `free` or `problem-guided` mode.

Build a small mixed fragment set containing some grounding plus older, underused, external/unresolved or distant material and an occasional random jump. The reference sampler's exact ratios are experimental.

Then deliberately delay convergence and try several operations:

```text
seek remote structural similarities
combine mechanisms from different memories
invert roles, assumptions or causal direction
transfer mechanisms across domains
change constraints in a counterfactual
follow strange connections
produce multiple variants
```

Return to normal reasoning after divergence.

Record useful outputs under `~/.ena/evolution/candidates/speculative/` with `truth_status: speculative`. `tools/candidate_record.py` provides a reference path for this.

Never write Dream-generated material directly into factual memory.

## 6. Touch reality

```text
candidate
→ normal reasoning
→ research / observation / real task / bounded trial
→ SAFE-CHANGE.md if critical runtime state changes
→ retain / revise / reject / restore
→ record the outcome
```

A candidate that survives reality contact may be recorded under `candidates/selected/`. Later Sleep runs decide how verified outcomes should affect durable memory.

Preserve negative and null results.

## 7. Add scheduling only after the manual path works

Ask the user to confirm cadence and cost limits. Use the Host scheduler when available and respect per-run limits.

## 8. Reference tools

Use confirmed settings rather than copying example values. See `tools/README.md` for commands.
