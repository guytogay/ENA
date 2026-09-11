# Sleep and Dream

Sleep and Dream are experimental offline evolution jobs for a long-lived Agent.

- **Sleep** consolidates accumulated experience into cleaner, better-connected durable memory.
- **Dream** recombines material that normal task retrieval would not usually place together and creates speculative candidates.
- **Reality** decides what survives. Dream output is never factual memory merely because it was generated.

Use `SLEEP-DREAM-QUICKSTART.md` for the first run.

## Experimental boundary

Fragment counts, sampling weights, distance bands and cadence in examples/reference tools are field parameters, not ENA requirements. Change them when evidence from the actual Host suggests a better setting.

Negative and null results are evidence. Do not expand Dream modes or sampling complexity merely because an additional mechanism sounds plausible.

## 1. Required inputs

Before enabling these jobs, identify:

- durable memory sources;
- experience/history sources, including earlier sessions when the Host can expose them;
- how memory is retrieved/indexed and changed;
- how a mistaken memory update can be reversed;
- a scheduler/idle/event mechanism when available;
- sources that must be excluded;
- the current capability inventory when available: tools, skills, connectors/plugins, APIs and other callable mechanisms;
- discoverable capabilities that are available to install/enable but are not currently active.

Keep the real long-term memory where the Host already keeps it. Do not duplicate it solely for ENA.

## 2. Cross-session scope

Sleep and Dream are not limited to the current conversation.

Past sessions, task history, conversation history, project records and future sessions may all become material when the Host or an authorized integration makes them accessible. Preserve enough provenance to distinguish directly experienced material from user-reported, document-derived, Agent-derived or inferred material.

Do not assume inaccessible sessions can be recovered. Record that limitation instead of inventing continuity.

Future sessions naturally join the same loop: useful events enter experience/history; later Sleep consolidates them; later Dream may recombine them with much older material.

Full transcripts are not required. Stable references, indexed records or concise experience fragments are preferable when they preserve enough context.

## 3. Capture useful experience while awake

If the Host does not already preserve an equivalent durable record, keep concise experience records for things likely to matter later, such as user corrections, repeated failures/successes, surprising outcomes, useful procedures, unresolved problems, important exceptions, lessons from another Agent, and evolution/safe-change outcomes.

Do not dump full conversations by default. Keep enough provenance to recover why an occurrence matters.

## 4. Sleep

Sleep is memory maintenance, not a daily summary.

Read new experience plus only the older memory needed to resolve duplication, contradiction, stale knowledge, overreach, reusable procedure, boundaries, unresolved questions or missing links.

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

Before durable writes, preserve a reversible previous state using the memory system's version/history/snapshot mechanism. If memory controls startup, communication, tool access or recovery, use `SAFE-CHANGE.md` as well.

After writing, verify that memory remains readable, changed records resolve, useful provenance/counterexamples remain reachable, and a new revision/version is recorded. Restore the previous state if verification fails.

A prettier summary is not a successful Sleep run if later retrieval/behavior is unchanged.

## 5. Dream

Dream is a variation generator. It should defeat ordinary nearest-neighbor retrieval without becoming pure noise.

Dream does not directly write generated claims into factual memory and does not directly modify the live Agent.

### Modes

```text
free             explore without a required problem anchor
problem-guided   start from one unresolved problem, then draw most additional material from distant memory
```

### Material pools

Eligible pools may include:

```text
recent       recent experience/memory
old          substantially older memory
underused    rarely retrieved/activated memory
external     learned from a user, document, A2A peer or other outside source
unresolved   unanswered question, contradiction or failed approach
salient      surprising/high-consequence/repeatedly reinforced memory
distant      non-nearest material by meaning/domain/source/time
capability   installed/enabled tools, skills, connectors, APIs or other real capabilities
possibility  discoverable capabilities that are not currently installed/enabled
random       unrestricted eligible material
```

Capability material must keep its real state. A discoverable but uninstalled skill/connector is a **possibility**, not a capability the Agent may silently assume it already has.

A Dream may propose combining a problem with a currently unavailable capability. Reality contact must verify that the capability still exists, can actually be installed/enabled, has the required authorization, and behaves as expected before selection.

### Sampling

Use a small mixed set with some recent grounding plus older/underused/external-or-unresolved/distant material and an occasional random jump. Capability/possibility material may participate when useful.

Choose probabilistically inside pools instead of always selecting the highest-scoring record. If vector similarity exists, derive close/middle/far bands from the local distribution rather than hard-coding a universal threshold. If vectors are unavailable, approximate distance using time, domain/project, source, tags/entities, task type and retrieval history.

Concrete proportions in examples/reference tools remain experimental defaults.

### Divergent exploration

Freeze the sampled set for a round and deliberately delay convergence. Try several operations before judging the ideas:

```text
seek remote structural similarities
combine mechanisms from different memories
reverse roles, assumptions or causal direction
transfer a mechanism across domains
combine a problem with an existing or discoverable capability
change constraints in a counterfactual
follow a strange connection longer than normal retrieval would
produce multiple variants
```

Keep generated content speculative during this stage.

### Candidate output

Return to normal reasoning and keep only useful hypotheses, mechanisms, questions, procedures, experiments, alternative explanations or possible self-improvements.

Dream-generated candidates belong under:

```text
~/.ena/evolution/candidates/speculative/
```

with `origin: dream` and `truth_status: speculative`. `tools/candidate_record.py` provides a reference writer.

Do not write Dream output into factual memory. A candidate that survives reality contact may move into the selected path, while factual/adaptive memory changes happen later through evidence-backed Sleep consolidation.

## 6. Return to reality

Candidates from Sleep or Dream follow `EVOLUTION.md`:

```text
candidate
→ normal reasoning
→ verify current capability/install/authorization state when relevant
→ research / observation / real task / bounded trial
→ SAFE-CHANGE.md when critical runtime state changes
→ retain / revise / reject / restore
→ production application if selected but not yet live
→ outcome becomes new experience
→ later Sleep consolidates what reality established
```

Do not create a separate selection system for Dream output.

## 7. Scheduling and limits

Sleep and Dream do not need human biological timing. Use user-confirmed or trusted-policy cadence/cost limits and the Host's existing scheduler when possible.

Respect explicit per-run limits for source material, generated candidates, wall-clock time and model/tool cost. Do not replay an unlimited backlog after missed runs.

## 8. Reference tools

The `tools/` directory contains conservative reference helpers for initialization, preflight, safe-change scaffolding, Sleep input preparation, Dream sampling and speculative candidate recording. Replace them with stronger Host-native mechanisms when available.
