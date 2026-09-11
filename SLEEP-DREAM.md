# ENA Sleep / Dream v0.1

Status: working draft — not Current.

Sleep and Dream are offline evolution workflows for a long-lived Agent.

- **Sleep** turns accumulated experience into cleaner, better-connected, more useful durable memory.
- **Dream** deliberately recombines memory that would not normally appear together and produces speculative evolution candidates.
- **Wake / Reality** decides what, if anything, survives contact with real work.

Dream output is not factual memory. Sleep may update durable memory, but only through a reversible write path.

## 1. Install the workflow during First Use

Before scheduling Sleep or Dream, identify the actual memory and scheduling mechanisms available on the Host.

Record or create:

```text
ENA.yaml
  -> evolution.sleep_dream_config

~/.ena/evolution/
  experience/
  candidates/
  runs/
    sleep/
    dream/
  locks/
  sleep-dream.yaml
```

The actual long-term memory may live elsewhere. Do not copy an existing Host memory system into `~/.ena/` merely to satisfy this layout. Store pointers to the real memory sources instead.

Configure at least:

- durable memory sources that Sleep may inspect;
- memory write/update method;
- version/history/snapshot method for reversible memory updates;
- experience inbox;
- candidate directory;
- scheduler or wake mechanism;
- excluded/sensitive memory sources;
- per-run resource limits;
- Sleep cadence;
- Dream cadence;
- Dream sampling policy.

A starting configuration is shown in [`examples/evolution/SLEEP-DREAM.example.yaml`](examples/evolution/SLEEP-DREAM.example.yaml).

## 2. Capture experience while awake

Sleep cannot consolidate experience that disappears before it reaches a durable source.

During normal work, put evolution-relevant occurrences into the experience inbox when they are not already durably represented by the Host.

Useful inputs include:

- user corrections;
- repeated failures or successes;
- surprising outcomes;
- procedures that worked repeatedly;
- unresolved problems;
- important exceptions or counterexamples;
- A2A lessons received from another Agent;
- ACMS/evolution outcomes;
- ideas worth reconsidering later.

Do not turn the inbox into a transcript dump. Store enough context and provenance to recover why the occurrence may matter.

A minimal experience record may contain:

```yaml
occurred_at: 2026-09-12T00:30:00+08:00
source_type: user_correction
source_ref: conversation-or-host-reference
summary: "The previous assumption about X was wrong under condition Y."
importance_hint: medium
unresolved: false
```

`importance_hint` is only an input signal. It does not grant the record permanent memory status.

## 3. Sleep Run

A Sleep Run is a consolidation job, not a daily summary.

### 3.1 Acquire a run lock

Allow only one durable memory-maintenance run to write the same memory scope at a time.

If another Sleep, memory migration, restore, or equivalent writer owns the scope, do not race it. Skip or defer the run according to the Host's normal scheduler behavior.

Create a run record under:

```text
~/.ena/evolution/runs/sleep/<timestamp>__<short-id>/
```

Record the canonical timezone, start time, memory sources, current memory revision/version if available, and resource limits.

### 3.2 Select material

Read:

1. new experience since the last successful Sleep Run;
2. currently active durable memories touched by those experiences;
3. older memories needed to resolve a contradiction, merge a cluster, or preserve a boundary;
4. unresolved material explicitly scheduled for reconsideration.

Do not load the entire lifetime archive by default. Expand only when the current consolidation question requires it.

### 3.3 Detect consolidation opportunities

Look for concrete opportunities such as:

```text
REPEAT      independent experiences support the same useful pattern
DUPLICATE   multiple records represent the same knowledge
FRAGMENT    useful knowledge is split across isolated records
CONFLICT    current memories disagree
STALE       a memory is superseded or its environment changed
OVERBROAD   a lesson generalized beyond its evidence
PROCEDURE   repeated successful behavior can become a reusable procedure
BOUNDARY    a counterexample or exception limits an existing rule
UNRESOLVED  repeated evidence still does not settle the question
LINK        distant records should become mutually reachable
```

These labels are operational hints, not required permanent memory classes.

### 3.4 Produce a consolidation plan before writing

Do not edit durable memory while still exploring what should change.

First produce a plan containing only proposed operations, source references, intended result, and uncertainty.

Typical operations:

```text
ADD
MERGE
LINK
REFINE
CORRECT
STRENGTHEN
WEAKEN
DORMANT
SUPERSEDE
ARCHIVE
NO_CHANGE
CREATE_CANDIDATE
```

A plan entry should preserve provenance and any important counterevidence.

If evidence is ambiguous, prefer `NO_CHANGE`, a narrower memory, or an explicit unresolved record over manufacturing certainty.

### 3.5 Protect the memory state

Before applying the consolidation plan, preserve a reversible prior state using the real memory system's history/version/snapshot mechanism.

If the memory being changed controls startup, recovery, A2A, tool access, communication, or another body-critical path, protect the change through ACMS rather than relying only on memory history.

Do not destroy provenance merely because the active representation is being compacted.

### 3.6 Apply the plan

Apply only the reviewed plan for this run.

Where the Host supports it, update more than prose records when appropriate, for example:

- retrieval priority;
- links/associations;
- cue-to-procedure mappings;
- salience or activation hints;
- status such as active/dormant/superseded;
- indexes used by future retrieval.

Do not pretend a rewritten summary changed future behavior if the actual memory/retrieval system still routes around it.

### 3.7 Verify and close

After writes:

- confirm the memory store remains readable;
- confirm changed records resolve correctly;
- confirm important provenance/counterexamples remain reachable;
- record the new revision/version;
- record what changed and what was intentionally left unresolved;
- release the lock.

If verification fails, restore the pre-Sleep state and mark the run failed.

A successful Sleep Run leaves a better memory substrate, not merely a prettier report.

## 4. Dream Run

Dream is a variation generator. It should deliberately defeat ordinary nearest-neighbor retrieval without collapsing into pure noise.

Dream never writes generated claims directly into factual memory.

### 4.1 Choose a Dream mode

Use one of two starting modes:

```text
FREE
  No required problem anchor. Explore unexpected connections in accumulated memory.

PROBLEM
  Start from one unresolved problem/question, then deliberately draw most additional material from distant memory rather than nearest-neighbor retrieval.
```

A scheduler may normally use `FREE`; an Agent stuck on a durable problem may explicitly invoke `PROBLEM`.

### 4.2 Build sampling pools

Construct candidate pools from memory available to the Agent. A practical v0.1 mix is:

```text
RECENT        recent experience or memory
OLD           substantially older memory
UNDERUSED     rarely retrieved or rarely activated memory
EXTERNAL      learned from user/document/A2A/other source rather than directly experienced
UNRESOLVED    unanswered question, contradiction, failed approach, dormant candidate
SALIENT       high-consequence, surprising, or repeatedly reinforced memory
DISTANT       semantically/structurally non-nearest material
RANDOM        unrestricted eligible memory
```

The same record may qualify for more than one pool. Avoid selecting the same fragment twice in one Dream set unless repetition itself is being explored.

### 4.3 Exclude material that should not enter Dream

Before sampling, remove or redact material that must not be recombined or reproduced outside its allowed context, including Host-marked secrets, credentials, private payloads, legally restricted material, or data excluded by local policy.

Use a safe abstract representation when the structural lesson is useful but the raw content is not.

### 4.4 Sample with biased randomness

Pure nearest-neighbor retrieval produces ordinary reasoning. Pure random retrieval produces too much noise.

Use biased randomness.

A practical default Dream set contains 5–7 fragments:

```text
1 recent
1 old
1 underused
1 external or unresolved
1 distant
0–1 salient
0–1 random jump
```

Choose within each pool probabilistically rather than always taking the highest-scoring item.

Recommended qualitative weighting:

```text
increase probability for:
  old but still valid/relevant material
  low retrieval frequency
  unresolved material
  surprising/high-consequence material
  cross-domain distance
  provenance diversity

decrease probability for:
  fragments used in very recent Dream Runs
  near-duplicates
  repeatedly dominant memories that already appear in normal retrieval
```

Add a small unrestricted random-jump probability so some Dream sets contain a relationship normal retrieval would never propose.

### 4.5 Use associative distance when available

If the Host exposes embedding/vector similarity, do not select only nearest neighbors.

For fragments chosen relative to an anchor:

1. exclude exact/near duplicates;
2. reserve a minority of close material so the Dream remains grounded;
3. prefer a middle-distance band for most associative jumps;
4. occasionally sample from the far tail as a random jump.

Do not hard-code one universal cosine threshold across embedding models. Derive bands from the distribution available on the Host, for example by similarity quantiles.

A useful starting policy is:

```text
close grounding:       top 10–25% similarity, small share
associative middle:    middle 40–70% of eligible distribution, largest share
far/random jump:       low-similarity tail or unrestricted random, small share
```

If vector similarity is unavailable, approximate distance using differences in time, project/domain, source, tags, entities, task type, and retrieval history.

### 4.6 Apply the Divergent Explorer operator

Once the Dream set is frozen for the round, temporarily optimize for variation rather than convergence.

The Dreaming Agent should:

```text
DELAY CONVERGENCE
Do not immediately choose the most plausible explanation.

SEARCH REMOTE STRUCTURAL CONNECTIONS
Look for shared structure even when vocabulary and domain differ.

HYBRIDIZE
Combine mechanisms or partial solutions from different memories.

INVERT
Reverse roles, directions, assumptions, dependencies, or causal order.

TRANSFER
Ask whether a mechanism from one domain can solve a structurally similar problem elsewhere.

COUNTERFACTUALIZE
Imagine changed constraints or environments.

FOLLOW STRANGE CONNECTIONS
Spend some effort on a connection precisely because ordinary retrieval would normally discard it.

GENERATE MULTIPLE VARIANTS
Do not let the first coherent idea terminate the Dream Run.
```

During this stage, generated statements remain speculative. Do not browse, execute external side effects, mutate the live Agent, or silently update factual memory merely to make the dream internally consistent.

### 4.7 Extract candidates, not dream prose

At the end of divergence, switch back to normal reasoning.

Discard most of the dream narrative.

Extract only candidate objects that create a potentially useful new search direction, such as:

- a hypothesis;
- a design or mechanism;
- a new question;
- a possible procedure;
- a proposed experiment;
- a suspected connection worth checking;
- an alternative explanation;
- a possible self-improvement.

Each candidate should include:

```yaml
origin: dream
mode: free_or_problem
source_fragments:
  - stable-memory-reference
  - stable-memory-reference
novel_connection: "..."
candidate: "..."
why_it_might_matter: "..."
reality_check: "What could be checked or tried next?"
truth_status: speculative
```

Store useful candidates in the normal Evolution candidate pool. Deduplicate against existing candidates when practical.

No candidate becomes selected merely because the Dreaming Agent finds it elegant.

### 4.8 Record the run and release the lock

Record:

- source fragment references and provenance classes;
- sampling pool used for each fragment;
- Dream mode;
- sampling/temperature settings;
- candidates emitted;
- candidates discarded as duplicates or noise;
- run cost/time if available.

Release the Dream lock.

## 5. Dream temperature

Use a small number of configurable temperature profiles rather than pretending one numeric value is universal across Hosts.

```text
LOW
  More grounding, fewer far jumps. Useful for practical variation around a known problem.

MEDIUM
  Default. Strong middle-distance recombination with occasional far jumps.

HIGH
  More underused/far/random material. Useful when ordinary reasoning repeatedly converges without solving the problem.
```

A Host may map these profiles to model temperature, retrieval sampling, embedding-distance bands, random-jump probability, or a combination.

Raising Dream temperature increases variation pressure, not truth confidence.

## 6. Wake / Reality selection

Sleep can create a candidate when consolidation exposes a possible improvement. Dream can create candidates through recombination.

Both feed the same Evolution path:

```text
candidate
  -> normal reasoning resumes
  -> research / observation / real task / bounded experiment
  -> ACMS when the Agent body is changed
  -> retain / revise / reject / restore
  -> outcome enters experience
  -> later Sleep consolidates what reality established
```

Do not create a second selection system specifically for dreams.

## 7. Scheduling

Sleep and Dream do not require human biological timing.

Ask the user to confirm a cadence appropriate to the Host and cost envelope, then persist it in `sleep-dream.yaml` and the actual scheduler.

A useful initial deployment may use:

```text
Sleep:
  periodic or after enough new experience accumulates

Dream:
  less frequent than Sleep
  plus explicit problem-triggered invocation when a durable problem remains stuck
```

If the Host exposes reliable idle/event scheduling, it may be preferable to a fixed clock schedule. Use the canonical timezone from `ENA.yaml` for clock-based schedules.

A missed Sleep or Dream window does not justify replaying an unbounded backlog. Process the most decision-relevant accumulated material within the current run limits.

## 8. Resource bounds

Every run should have explicit limits appropriate to the Host, such as:

```text
maximum source fragments
maximum input tokens/bytes
maximum generated candidates
maximum wall-clock duration
maximum model/tool cost
```

When the limit is reached, leave remaining material for a later run rather than silently expanding the job.

The default v0.1 examples are deliberately small so an adopter can observe the mechanism before increasing scale.

## 9. Failure behavior

Sleep failure:

```text
no verified durable memory update
  -> restore the pre-run memory state when necessary
  -> mark run failed
  -> preserve enough error information for later repair
```

Dream failure:

```text
no factual-memory mutation occurred
  -> mark run failed or partial
  -> keep only clearly delimited speculative candidates that were completely written
```

Scheduler failure should not block normal awake work unless the Host itself depends on the same failed component.

## 10. What to observe in early use

This v0.1 is intended to become better from field use.

Useful feedback includes whether:

- Sleep actually reduces fragmentation/contradiction and improves later retrieval/application;
- useful learned procedures survive across sessions;
- Sleep overcompresses nuance or creates dogma;
- Dream produces candidates ordinary retrieval would not have produced;
- Dream becomes repetitive, noisy, or too dominated by recent/high-salience memory;
- far/random sampling produces valuable novelty or mostly waste;
- problem-triggered Dream helps when normal reasoning repeatedly converges;
- speculative dream content ever leaks into factual memory;
- the cadence and run limits fit the Host's actual cost and workload.

Do not evaluate Dream mainly by whether its prose appears creative. Evaluate whether it creates useful candidate variation that later survives reality contact.
