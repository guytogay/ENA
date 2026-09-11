# Sleep and Dream

Sleep and Dream are experimental offline evolution jobs for a long-lived Agent.

- **Sleep** consolidates accumulated experience into cleaner, better-connected durable memory.
- **Dream** recombines memories that normal task retrieval would not usually place together and creates speculative candidates.
- **Reality** decides what survives. Dream output is never factual memory merely because it was generated.

Use `SLEEP-DREAM-QUICKSTART.md` for the first run.

## Experimental boundary

The current fragment counts, sampling weights, distance bands and cadence in examples/reference tools are **field parameters, not ENA requirements**. Change them when evidence from the actual Host suggests a better setting.

Useful evidence includes:

- later retrieval/behavior improves after Sleep;
- a Dream candidate survives reality contact;
- Sleep overcompresses nuance or damages useful boundaries;
- Dream is repetitive or mostly noise;
- a run produces no useful candidate;
- speculative Dream material leaks toward factual memory.

Negative and null results are evidence. Do not expand Dream modes or sampling complexity merely because an additional mechanism sounds plausible.

## 1. Required inputs

Before enabling these jobs, identify:

- durable memory sources;
- experience/history sources;
- how memory is retrieved/indexed;
- how durable memory can be changed;
- how a mistaken memory update can be reversed;
- a scheduler/idle/event mechanism when available;
- memory sources that must be excluded.

A typical local work area is:

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
  sleep-dream.yaml
```

Keep the real long-term memory where the Host already keeps it. Do not duplicate it solely for ENA.

## 2. Capture useful experience while awake

If the Host does not already preserve an equivalent durable record, add concise experience records for things likely to matter later:

- user corrections;
- repeated failures/successes;
- surprising outcomes;
- useful repeated procedures;
- unresolved problems;
- important exceptions/counterexamples;
- lessons received from another Agent;
- outcomes from evolution or safe self-change;
- ideas worth revisiting.

Do not dump full conversations by default. Keep enough provenance to recover why an occurrence matters.

## 3. Sleep

Sleep is memory maintenance, not a daily summary.

### Select material

Read new experience, the active memories those experiences touch, older memories needed to resolve contradiction/merge/preserve boundaries, and explicitly unresolved material. Do not load the whole lifetime archive by default.

### Find useful memory changes

Look for:

```text
repetition
duplication
fragmentation
conflict
staleness
overreach
reusable procedure
counterexample/boundary
unresolved question
missing association
```

### Plan before writing

Produce a consolidation plan before changing durable memory. Useful operations include:

```text
add
merge
link
refine
correct
strengthen
weaken
mark dormant
supersede
archive
leave unchanged
create an evolution candidate
```

Keep source references, intended result and important uncertainty/counterevidence. When evidence is ambiguous, prefer a narrower memory, an unresolved record or no change over manufactured certainty.

### Preserve and apply

Before durable writes, preserve a reversible previous state using the memory system's version/history/snapshot mechanism. If the memory controls startup, communication, tool access or recovery, use `SAFE-CHANGE.md` as well.

Apply only the planned operations. When supported, update mechanisms that actually influence future retrieval/behavior rather than only rewriting prose.

### Verify

Confirm memory remains readable, changed records resolve, useful provenance/counterexamples remain reachable, and the new revision/version is recorded. Restore the pre-Sleep state if verification fails.

A prettier summary is not a successful Sleep run if later retrieval/behavior is unchanged.

## 4. Dream

Dream is a variation generator. It should defeat ordinary nearest-neighbor retrieval without becoming pure noise.

Dream does not directly write generated claims into factual memory and does not directly modify the live Agent.

### Choose a mode

```text
free             explore without a required problem anchor
problem-guided   start from one unresolved problem, then draw most additional material from distant memory
```

These are the current field modes, not a claim that all useful Dream modes have been discovered.

### Build memory pools

Eligible pools may include:

```text
recent       recent experience/memory
old          substantially older memory
underused    rarely retrieved/activated memory
external     learned from a user, document, A2A peer or other outside source
unresolved   unanswered question, contradiction or failed approach
salient      surprising/high-consequence/repeatedly reinforced memory
distant      non-nearest material by meaning/domain/source/time
random       unrestricted eligible memory
```

Remove/redact secrets, credentials, private payloads and material excluded by local policy.

### Sample with biased randomness

Use a **small mixed set** that deliberately includes some recent grounding plus older/underused/external-or-unresolved/distant material and an occasional random jump.

Choose probabilistically inside pools instead of always selecting the highest-scoring record. Reduce repeated use of near-duplicates and memories that already dominate normal retrieval.

If vector similarity exists, derive close/middle/far bands from the local similarity distribution rather than hard-coding a universal cosine threshold. Prefer middle-distance material for many associative jumps while retaining some grounding and occasional far/random material.

If vectors are unavailable, approximate distance with time, domain/project, source, tags/entities, task type and retrieval history.

Concrete proportions in `examples/evolution/SLEEP-DREAM.example.yaml` and `tools/dream_sample.py` are experimental defaults for field use, not normative values.

### Perform divergent exploration

Freeze the sampled set for the round, then deliberately delay convergence. Do several of these before judging the ideas:

```text
seek remote structural similarities
combine partial mechanisms from different memories
reverse roles, direction, assumptions or causal order
transfer a mechanism from one domain to another
change constraints in a counterfactual scenario
follow a strange connection longer than normal retrieval would
produce multiple variants instead of stopping at the first coherent one
```

Keep generated content speculative during this stage.

### Extract candidates into the speculative path

Return to normal reasoning and discard most dream prose. Keep only potentially useful hypotheses, mechanisms, questions, procedures, experiments, alternative explanations or possible self-improvements.

Dream-generated candidates must be recorded under:

```text
~/.ena/evolution/candidates/speculative/
```

with:

```yaml
origin: dream
truth_status: speculative
source_fragments: []
candidate: "..."
reality_check: "..."
```

Use `tools/candidate_record.py --origin dream ...` when using the reference tools. That helper always writes Dream candidates into the speculative directory and sets `truth_status: speculative`.

Do not write Dream output into factual memory. A candidate that later survives reality contact may be recorded under `candidates/selected/`, but factual/adaptive memory changes still happen through normal reality evidence and later Sleep consolidation.

## 5. Return to reality

Candidates from Sleep or Dream follow `EVOLUTION.md`:

```text
candidate
→ normal reasoning
→ research / observation / real task / bounded trial
→ SAFE-CHANGE.md when critical runtime state changes
→ retain / revise / reject / restore
→ outcome becomes new experience
→ later Sleep consolidates what reality established
```

Do not invent a separate selection system for Dream output.

## 6. Scheduling and limits

Sleep and Dream do not need human biological timing. Ask the user to confirm a cadence/cost envelope and use the Host's existing scheduler when possible.

Sleep will often be more frequent than Dream; problem-guided Dream is useful when ordinary reasoning repeatedly converges without resolving a durable problem. Treat that as a field starting point, not a universal law.

Respect explicit per-run limits for source material, generated candidates, wall-clock time and model/tool cost. Do not replay an unlimited backlog after missed runs.

## 7. Reference tools

The `tools/` directory contains conservative reference helpers for initialization, preflight, safe-change scaffolding, Sleep input preparation, Dream sampling and speculative candidate recording. Replace them with stronger Host-native mechanisms when available.
