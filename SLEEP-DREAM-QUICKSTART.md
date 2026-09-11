# Sleep / Dream v0.1 Quickstart

Use this after `FIRST-USE.md` has identified the real Host, memory sources, canonical timezone/language, and ENA home.

## 1. Create the local working directories

Under the configured ENA home, create:

```text
~/.ena/evolution/
  experience/
  candidates/
  runs/
    sleep/
    dream/
  locks/
```

Keep the real long-term memory where the Host already keeps it. Record pointers; do not duplicate it only for ENA.

## 2. Create `sleep-dream.yaml`

Start from `examples/evolution/SLEEP-DREAM.example.yaml`.

Fill in:

- actual memory sources;
- how durable memory can be updated;
- how the previous memory state can be recovered;
- sources that Sleep/Dream must not read;
- Sleep and Dream run limits;
- scheduler/task references when they exist.

Keep the canonical timezone and language aligned with `ENA.yaml`.

## 3. Start feeding the experience inbox

When normal work produces a correction, repeated success/failure, surprising outcome, unresolved problem, useful procedure, ACMS/evolution result, or other experience worth later digestion, preserve a concise record in `~/.ena/evolution/experience/` if the Host does not already provide an equivalent durable record.

Do not dump whole conversations by default.

## 4. Run Sleep manually once

Read `SLEEP-DREAM.md` section `Sleep Run`, then execute this sequence:

```text
lock memory-maintenance scope
→ collect new experience + relevant existing memory
→ find repeat/duplicate/conflict/stale/overbroad/procedure/boundary/unresolved/link opportunities
→ write a consolidation plan without changing durable memory
→ preserve a reversible pre-run memory state
→ apply only the planned changes
→ verify memory remains readable and provenance/boundaries remain reachable
→ record the run
→ unlock
```

If verification fails, restore the pre-run memory state.

The output should be changed memory/retrieval behavior, not just a summary report.

## 5. Run Dream manually once

Choose either:

```text
FREE    explore without a required problem anchor
PROBLEM explore around one unresolved problem
```

Build one Dream set of 5–7 eligible fragments using a mixture of:

```text
recent
old
underused
external or unresolved
distant
optional salient
optional random jump
```

Then execute the Divergent Explorer operator from `SLEEP-DREAM.md`:

```text
delay convergence
→ seek remote structural connections
→ hybridize
→ invert
→ transfer mechanisms across domains
→ counterfactualize
→ follow strange connections
→ generate multiple variants
```

Return to normal reasoning after divergence.

Keep only useful speculative candidates. Do not write dream-generated claims into factual memory.

Store candidates under `~/.ena/evolution/candidates/` using the normal `EVOLUTION.md` candidate path.

## 6. Wake and touch reality

For any candidate worth pursuing:

```text
candidate
→ normal reasoning
→ research / observation / real task / bounded trial
→ ACMS when the Agent body changes
→ retain / revise / reject / restore
→ preserve outcome as new experience
```

Later Sleep Runs consolidate what reality established.

## 7. Add scheduling after the manual path is understood

Ask the user to confirm an appropriate cadence and cost envelope.

A reasonable first deployment is:

```text
Sleep: more frequent
Dream: less frequent
Problem Dream: explicit invocation when normal reasoning repeatedly converges without resolving a durable problem
```

Use the Host's existing scheduler when available. Record the actual scheduler references in the local configuration.

Do not replay an unlimited backlog after missed runs. Respect the configured per-run bounds.

## 8. Send feedback

Useful field feedback is concrete:

```text
what Host/memory substrate was used
what Sleep changed
whether later retrieval/behavior improved or degraded
what Dream fragments were sampled
what candidate was novel
whether ordinary reasoning likely would have produced it anyway
what happened when the candidate touched reality
cost/noise/failure modes
```

Preserve negative and null results. A Dream that produced nothing useful is still evidence about the sampler/operator/cadence.
