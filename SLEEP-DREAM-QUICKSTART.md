# Sleep / Dream Quickstart

Use this after `FIRST-USE.md` has identified the real Host, memory sources, timezone/language and ENA home.

## 1. Create the working directories

```text
~/.ena/evolution/
  experience/
  candidates/
  runs/
    sleep/
    dream/
  locks/
```

Keep the real long-term memory where the Host already keeps it.

## 2. Create `sleep-dream.yaml`

Start from `examples/evolution/SLEEP-DREAM.example.yaml` and fill in:

- actual memory sources;
- memory write/update method;
- how the previous memory state can be restored;
- excluded sources;
- run limits;
- scheduler references when available.

Keep timezone/language aligned with `ENA.yaml`.

## 3. Feed useful experience

When normal work produces a correction, repeated success/failure, surprising outcome, unresolved problem, useful procedure or evolution result, preserve a concise record in `~/.ena/evolution/experience/` if the Host does not already provide an equivalent durable record.

Do not dump whole conversations by default.

## 4. Run Sleep once manually

```text
lock the memory-maintenance scope
→ collect new experience + only relevant existing memory
→ find duplication/conflict/staleness/overreach/procedures/boundaries/unresolved links
→ write a consolidation plan without changing memory
→ preserve a reversible pre-run state
→ apply only the plan
→ verify memory + provenance remain usable
→ record the run
→ unlock
```

If verification fails, restore the pre-run memory state.

The result should improve real memory/retrieval behavior, not merely create a summary.

## 5. Run Dream once manually

Choose:

```text
free             no required problem anchor
problem-guided   one unresolved problem as anchor
```

Build a 5–7 fragment set using a mixture of:

```text
recent
old
underused
external or unresolved
distant
optional salient
optional random jump
```

Then deliberately delay convergence and try several operations:

```text
seek remote structural similarities
combine mechanisms from different memories
invert roles/assumptions/causal direction
transfer mechanisms across domains
change constraints in a counterfactual
follow strange connections
produce multiple variants
```

Return to normal reasoning after divergence.

Keep only useful speculative candidates. Never promote dream-generated material directly into factual memory.

## 6. Touch reality

For a candidate worth pursuing:

```text
candidate
→ normal reasoning
→ research / observation / real task / bounded trial
→ SAFE-CHANGE.md if critical runtime state changes
→ retain / revise / reject / restore
→ preserve the outcome as new experience
```

Later Sleep runs consolidate what reality established.

## 7. Add scheduling

Ask the user to confirm cadence and cost limits.

A simple start:

```text
Sleep: more frequent
Dream: less frequent
problem-guided Dream: invoke when ordinary reasoning repeatedly converges without resolving a durable problem
```

Use the Host scheduler when available. Respect per-run limits rather than replaying an unlimited backlog.

## 8. Optional reference tools

```text
python tools/ena_init.py --timezone Asia/Shanghai --language zh-CN
python tools/dream_sample.py --memory memories.jsonl --output dream-set.json
python tools/new_change.py --name fix-config --target /path/to/config
```

These are reference implementations. Replace them with stronger Host-native mechanisms when available.
