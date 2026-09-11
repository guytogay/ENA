# Reference tools

These scripts use only the Python standard library. An Agent can run them as examples and replace them with stronger Host-native mechanisms later.

```text
ena_init.py                 create ENA.yaml, SYSTEM.yaml and working directories
ena_preflight.py            fail fast when First Use is missing/not ready/stale
change_scaffold.py          create a timestamped safe-change package skeleton
sleep_prepare.py            build a bounded Sleep input bundle from JSONL records
combine_dream_material.py   combine memory + knowledge + capability material
dream_sample.py             sample a Dream set with biased randomness / distance
candidate_record.py         write new candidates only into the speculative path
self_test.py                verify the reference tools against included sample data
```

## Verify the tools

```bash
python tools/self_test.py
```

Expected output:

```text
ENA reference tools: OK
```

## Initialize interactively or from policy

When values are being confirmed during First Use:

```text
python tools/ena_init.py --timezone CONFIRMED_IANA_TIMEZONE --language CONFIRMED_LANGUAGE_TAG
```

This creates `SYSTEM.yaml` with `minimum_ready: false`. Verify a real recovery path and rescuer before marking it ready.

For a trusted deployment/workspace policy that already verified the minimum, the same tool can initialize non-interactively:

```text
python tools/ena_init.py \
  --timezone CONFIRMED_IANA_TIMEZONE \
  --language CONFIRMED_LANGUAGE_TAG \
  --host-profile session \
  --recovery VERIFIED_RECOVERY_REFERENCE \
  --rescuer VERIFIED_RESCUER_REFERENCE \
  --rescuer-type human \
  --verified-minimum
```

`--verified-minimum` is not automatic proof. The caller is asserting that the supplied recovery path and rescuer were actually verified. Missing policy values should remain unresolved rather than being filled with product defaults.

## Preflight at session/startup time

```bash
python tools/ena_preflight.py
```

Configure the Host to run this before ordinary Agent work when a startup/session hook exists. Exit code `2` means First Use must be completed/refreshed before continuing.

## Create a safe-change package

Choose the Host profile from `SAFE-CHANGE.md`:

```text
python tools/change_scaffold.py --name fix-config --timezone CONFIRMED_IANA_TIMEZONE --profile session
```

or use `--profile resident` for a long-running service/daemon style Agent.

The scaffold does not edit live state and does not pretend one universal rollback scheduler is reliable on every Host. Fill it with the profile-appropriate restore path from `SAFE-CHANGE.md`.

For a directly usable session/coding example based on Git branch + worktree + revert, see:

```text
examples/change/SESSION-GIT-WORKTREE.md
```

## Prepare a Sleep input bundle

```bash
python tools/sleep_prepare.py \
  --experience examples/evolution/EXPERIENCE.example.jsonl \
  --memory examples/evolution/MEMORY.example.jsonl \
  --output sleep-input.json
```

Give the bundle to the Agent/model and apply the consolidation steps in `SLEEP-DREAM.md`.

## Combine Dream material from multiple sources

`dream_sample.py` accepts one JSONL stream. Use the combiner when the Dream should include authorized knowledge-base material and the Agent's capability surface as well as memory/session history:

```bash
python tools/combine_dream_material.py \
  --memory examples/evolution/MEMORY.example.jsonl \
  --knowledge examples/evolution/KNOWLEDGE.example.jsonl \
  --capabilities examples/evolution/CAPABILITIES.example.jsonl \
  --output dream-material.jsonl
```

Capability records should preserve whether the capability is actually installed/verified, merely advertised by an Agent Card, or only discoverable but not enabled. Do not convert an advertised or catalog capability into a real ability merely by including it in Dream material.

## Sample a free Dream

```bash
python tools/dream_sample.py \
  --memory dream-material.jsonl \
  --output dream-set.json \
  --seed 42
```

## Sample a problem-guided Dream

```bash
python tools/dream_sample.py \
  --memory dream-material.jsonl \
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
