# Reference tools

These scripts use only the Python standard library. An Agent can run them as examples and replace them with stronger Host-native mechanisms later.

```text
ena_init.py          create ENA.yaml, SYSTEM.yaml and working directories
ena_preflight.py     fail fast when First Use is missing/not ready/stale
change_scaffold.py   create a timestamped safe-change package skeleton
sleep_prepare.py     build a bounded Sleep input bundle from JSONL records
dream_sample.py      sample a Dream set with biased randomness / distance
candidate_record.py  write new candidates only into the speculative path
self_test.py         verify the reference tools against included sample data
```

## Verify the tools

```bash
python tools/self_test.py
```

Expected output:

```text
ENA reference tools: OK
```

## Initialize

Use values the user has actually confirmed:

```text
python tools/ena_init.py --timezone CONFIRMED_IANA_TIMEZONE --language CONFIRMED_LANGUAGE_TAG
```

The initializer creates `SYSTEM.yaml` with `minimum_ready: false`. Complete the minimum First Use, record a real recovery path and rescuer, then set it true.

## Preflight at session/startup time

```bash
python tools/ena_preflight.py
```

Configure the Host to run this before ordinary Agent work when a startup/session hook exists. Exit code `2` means First Use must be completed/refreshed before continuing.

## Create a safe-change package

```text
python tools/change_scaffold.py --name fix-config --timezone CONFIRMED_IANA_TIMEZONE
```

The scaffold does not edit live state and does not pretend one universal rollback scheduler is reliable on every Host. Fill it with the profile-appropriate restore path from `SAFE-CHANGE.md`.

## Prepare a Sleep input bundle

```bash
python tools/sleep_prepare.py \
  --experience examples/evolution/EXPERIENCE.example.jsonl \
  --memory examples/evolution/MEMORY.example.jsonl \
  --output sleep-input.json
```

Give the bundle to the Agent/model and apply the consolidation steps in `SLEEP-DREAM.md`.

## Sample a free Dream

```bash
python tools/dream_sample.py \
  --memory examples/evolution/MEMORY.example.jsonl \
  --output dream-set.json \
  --seed 42
```

## Sample a problem-guided Dream

```bash
python tools/dream_sample.py \
  --memory examples/evolution/MEMORY.example.jsonl \
  --mode problem-guided \
  --anchor-id m4 \
  --output dream-set.json \
  --seed 42
```

The reference sampler's counts/weights are experimental field defaults, not ENA requirements.

## Record a speculative candidate

```text
python tools/candidate_record.py --origin dream --candidate "IDEA" --reality-check "CHECK"
```

The helper always writes to `~/.ena/evolution/candidates/speculative/` and sets `truth_status: speculative`. Generated claims remain separate from factual memory until reality contact produces evidence.
