# Reference tools

These small scripts use only the Python standard library. They are examples an Agent can run, inspect and adapt to its Host.

```text
ena_init.py         create the ENA home and base ENA.yaml
change_scaffold.py  create a timestamped safe-change package skeleton
sleep_prepare.py    build a bounded Sleep input bundle from JSONL records
dream_sample.py     sample a Dream set with biased randomness
```

Examples:

```bash
python tools/ena_init.py --timezone Asia/Shanghai --language zh-CN
python tools/change_scaffold.py --name fix-a2a --timezone Asia/Shanghai
python tools/sleep_prepare.py --experience experience.jsonl --memory memory.jsonl --output sleep-input.json
python tools/dream_sample.py --memory memory.jsonl --output dream-set.json --seed 42
```

The change scaffold intentionally does not edit live files or pretend to provide universal rollback scheduling. Fill the package with the real Host backup/restore mechanism described in `SAFE-CHANGE.md`.

The Sleep and Dream tools prepare bounded inputs; the Agent/model still performs consolidation or divergent reasoning. Host-native memory/search/snapshot/scheduler facilities should replace these reference helpers when they are stronger.
