# ENA

ENA helps an Agent inspect its environment, collaborate with other Agents, recover from failure, change itself reversibly, consolidate memory, generate new ideas, and test improvements against reality.

## Start here

Read and apply these in order:

1. `FIRST-USE.md` — inspect the real Agent/Host and confirm one timezone, language and ENA home.
2. `A2A.md` — reuse or establish a real two-way Agent-to-Agent path and rescue peer.
3. `SURVIVAL.md` — keep restart and recovery available outside the Agent process.
4. `SAFE-CHANGE.md` — preserve the previous working state and prepare recovery before an important self-change.
5. `EVOLUTION.md` — preserve an improvement candidate, test it against reality, and keep/revise/reject/restore it.
6. `SLEEP-DREAM-QUICKSTART.md` — run the first Sleep and Dream cycle. `SLEEP-DREAM.md` contains the full mechanism.

## Local files

A typical installation starts with:

```text
~/.ena/
  ENA.yaml
  SYSTEM.yaml
  changes/
  evolution/
```

Use `ENA.example.yaml` and `examples/SYSTEM.example.yaml` as starting points.

## Reference tools

The `tools/` directory contains small standard-library Python examples:

```text
ena_init.py
change_scaffold.py
sleep_prepare.py
dream_sample.py
self_test.py
```

Verify them with:

```bash
python tools/self_test.py
```

Then see `tools/README.md` for runnable examples. Prefer stronger Host-native backup, scheduler, snapshot, A2A or memory mechanisms when they already exist.
