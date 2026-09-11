# Reference tools

These scripts use only the Python standard library. An Agent can run them as examples and replace them with stronger Host-native mechanisms later.

```text
ena_init.py         create ENA.yaml, SYSTEM.yaml and working directories
change_scaffold.py  create a timestamped safe-change package skeleton
sleep_prepare.py    build a bounded Sleep input bundle from JSONL records
dream_sample.py     sample a Dream set with biased randomness / distance
self_test.py        verify the reference tools against included sample data
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

```bash
python tools/ena_init.py --timezone Asia/Shanghai --language zh-CN
```

## Create a safe-change package

```bash
python tools/change_scaffold.py --name fix-a2a --timezone Asia/Shanghai
```

The scaffold does not edit live files and does not pretend one universal rollback scheduler is reliable on every Host. Fill it with the real backup/restore/timer from `SAFE-CHANGE.md`.

## Prepare a Sleep input bundle

```bash
python tools/sleep_prepare.py \
  --experience examples/evolution/EXPERIENCE.example.jsonl \
  --memory examples/evolution/MEMORY.example.jsonl \
  --output sleep-input.json
```

Give the resulting bundle to the Agent/model and apply the consolidation steps in `SLEEP-DREAM.md`.

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

Use the sampled fragments with the divergent-exploration steps in `SLEEP-DREAM.md`. Generated claims remain speculative until they touch reality.
