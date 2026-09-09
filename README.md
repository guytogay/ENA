# ENA

ENA helps capable Agents improve, adapt, recover, and evolve through real work.

This repository is the clean product home for the next ENA. It is under active development and is **not yet the Current release**.

## Working core

The first product behavior is in [`CORE.md`](CORE.md).

It starts from two real failures observed in ENA v0.3.14 adopters and again during this rebuild:

- Agents can recognize actionable problems yet stop without a real blocker and wait for another human prompt.
- Agents can understand useful guidance, explain it correctly, and still fail to apply it to the work in front of them.

The working default is simple: **if there is a useful next step you can responsibly take now, take it; when new information changes what you should do, use it. Stop only for a real reason.**

Evidence and discussion:

- [Issue #1 — Actionable problems get deferred without a real blocker](https://github.com/guytogay/ENA/issues/1)
- [Issue #6 — Useful guidance gets acknowledged but not applied](https://github.com/guytogay/ENA/issues/6)

## Current release

The existing Current release remains `v0.3.14 / FIELD_VALIDATION` in the legacy architecture repository: `guytogay/evolution-native-agent-architecture`.
