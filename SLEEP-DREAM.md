# Sleep and Dream

Sleep and Dream are offline evolution jobs for a long-lived Agent.

- **Sleep** consolidates accumulated experience into cleaner, better-connected durable memory.
- **Dream** recombines memories that normal task retrieval would not usually place together and creates speculative candidates.
- **Reality** decides what survives. Dream output is never factual memory merely because it was generated.

Use `SLEEP-DREAM-QUICKSTART.md` for the first run.

## 1. Required inputs

Before enabling these jobs, First Use should have identified:

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

Do not dump full conversations by default. Keep enough context and provenance to recover why the occurrence matters.

Example:

```yaml
occurred_at: 2026-09-12T00:30:00+08:00
source_type: user_correction
source_ref: conversation-or-host-reference
summary: "The previous assumption about X was wrong under condition Y."
unresolved: false
```

## 3. Sleep

Sleep is memory maintenance, not a daily summary.

### Step 1 — lock the memory scope

Allow only one writer to maintain the same durable memory scope at a time. If another maintenance/migration/restore job owns the scope, skip or defer this run.

Create a run record under:

```text
~/.ena/evolution/runs/sleep/<timestamp>__<short-id>/
```

### Step 2 — select material

Read:

1. new experience since the previous successful Sleep run;
2. active memories touched by those experiences;
3. older memories needed to resolve a contradiction, merge a cluster or preserve a boundary;
4. unresolved material explicitly scheduled for reconsideration.

Do not load the entire lifetime archive by default.

### Step 3 — find useful memory changes

Look for:

```text
repetition      independent experience supports the same pattern
duplication     multiple records say the same thing
fragmentation   useful knowledge is split across isolated records
conflict        memories disagree
staleness       environment/evidence has changed
overreach       a lesson is broader than its evidence
procedure       repeated successful behavior can become reusable
boundary        a counterexample limits an existing rule
unresolved      evidence still does not settle the question
missing link    related memories should become mutually reachable
```

### Step 4 — plan before writing

Produce a consolidation plan first. Do not edit durable memory while still exploring what should change.

Useful operations are ordinary actions, not permanent memory classes:

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

For each planned change keep source references, intended result and important uncertainty/counterevidence.

When evidence is ambiguous, prefer a narrower memory, an unresolved record or no change over manufactured certainty.

### Step 5 — preserve the previous state

Before durable writes, create a reversible previous state using the memory system's own version/history/snapshot mechanism.

If the memory being changed controls startup, communication, tool access or recovery, use `SAFE-CHANGE.md` as well.

### Step 6 — apply the plan

Apply only the planned operations.

When the Host supports it, update mechanisms that actually influence future retrieval/behavior, not just prose, for example:

- retrieval priority;
- links/associations;
- cue-to-procedure mappings;
- active/dormant/superseded status;
- indexes used by later retrieval.

A prettier summary is not a successful Sleep run if the Agent still routes around it.

### Step 7 — verify

Confirm that:

- memory remains readable;
- changed records resolve;
- useful provenance and counterexamples remain reachable;
- the new revision/version is recorded.

If verification fails, restore the pre-Sleep state.

See `examples/evolution/SLEEP-RUN.example.yaml`.

## 4. Dream

Dream is a variation generator. It should defeat ordinary nearest-neighbor retrieval without becoming pure noise.

Dream does not directly write generated claims into factual memory and does not directly modify the live Agent.

### Step 1 — choose a mode

```text
free             explore without a required problem anchor
problem-guided   start from one unresolved problem, then draw most additional material from distant memory
```

### Step 2 — build memory pools

Eligible pools can include:

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

Remove/redact secrets, credentials, private payloads and other material local policy excludes from recombination.

### Step 3 — sample with biased randomness

A useful starting Dream set contains 5–7 fragments:

```text
1 recent
1 old
1 underused
1 external or unresolved
1 distant
0–1 salient
0–1 random jump
```

Choose probabilistically inside each pool instead of always selecting the highest-scoring record.

Increase probability for old/underused/unresolved/cross-domain material. Decrease probability for near-duplicates, material used in very recent Dream runs and memories that already dominate normal retrieval.

Keep a small unrestricted random-jump probability so some combinations can occur that ordinary retrieval would never propose.

### Step 4 — use associative distance when available

If vector similarity exists, do not select only nearest neighbors.

Relative to an anchor:

1. remove exact/near duplicates;
2. use a small amount of close material for grounding;
3. draw most associative jumps from a middle-distance band;
4. occasionally use the far tail/random sampling.

Do not hard-code one cosine-similarity threshold across embedding models. Derive close/middle/far bands from the local similarity distribution.

A starting proportion can be:

```text
close grounding     20%
middle distance     65%
far/random           15%
```

If vectors are unavailable, approximate distance with time, domain/project, source, tags/entities, task type and retrieval history.

### Step 5 — perform divergent exploration

Freeze the sampled set for the round, then deliberately delay convergence.

Do several of these before judging the ideas:

```text
seek remote structural similarities
combine partial mechanisms from different memories
reverse roles, direction, assumptions or causal order
transfer a mechanism from one domain to another
change constraints in a counterfactual scenario
follow a strange connection longer than normal retrieval would
produce multiple variants instead of stopping at the first coherent one
```

During this stage, do not browse/act merely to make the imagined story consistent. Keep generated content speculative.

### Step 6 — extract candidates

Return to normal reasoning and discard most dream prose.

Keep only potentially useful outputs such as:

- hypothesis;
- design/mechanism;
- new question;
- possible procedure;
- experiment;
- suspected connection worth checking;
- alternative explanation;
- possible self-improvement.

Example candidate fields:

```yaml
origin: dream
mode: problem-guided
source_fragments:
  - stable-memory-reference
  - stable-memory-reference
candidate: "..."
why_it_might_matter: "..."
reality_check: "What can be observed or tried next?"
truth_status: speculative
```

Store useful candidates in the normal evolution candidate directory. Deduplicate when practical.

See `examples/evolution/DREAM-RUN.example.yaml`.

## 5. Dream intensity

Use descriptive profiles rather than pretending one numeric value works across all Hosts:

```text
low      more grounding, fewer far jumps
medium   default; mostly middle-distance recombination
high     more old/underused/far/random material when normal reasoning is repeatedly stuck
```

The Host may implement this through model temperature, retrieval sampling, distance bands, random-jump probability or a combination.

Higher intensity means more variation, not more truth.

## 6. Return to reality

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

## 7. Scheduling

Sleep and Dream do not need human biological timing.

Ask the user to confirm a cadence/cost envelope and use the Host's existing scheduler when possible.

A reasonable first deployment:

```text
Sleep: more frequent, or after enough new experience accumulates
Dream: less frequent
problem-guided Dream: explicitly invoke when a durable problem remains stuck
```

Respect explicit per-run limits such as maximum fragments, generated candidates, wall-clock time and model/tool cost. Do not replay an unlimited backlog after missed runs.

## 8. Reference tools

The `tools/` directory contains small reference implementations for initialization, protected file changes and Dream sampling. They are intentionally conservative and can be replaced by stronger Host-native mechanisms.
