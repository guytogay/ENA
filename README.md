# ENA

ENA helps capable Agents gain practical capabilities they do not get from model reasoning alone.

This repository is the clean product home for the next ENA. It is under active development and is **not yet the Current release**.

## Current product direction

Do not rebuild ordinary model judgment inside ENA. A capable model can already reason about bugs, feedback, tradeoffs, changing requirements, and project drift.

ENA should add the missing machinery that lets those judgments become durable Agent capability.

The first active product work is concrete:

- [Issue #8 — build a survivable runtime](https://github.com/guytogay/ENA/issues/8): help an Agent use its Host to survive interruption, restart, bad self-change, and recovery.
- [Issue #9 — build an executable evolution system](https://github.com/guytogay/ENA/issues/9): help an Agent safely try changes, observe reality, keep useful improvements, reject or roll back bad ones, and carry learning forward.

Issues #1 and #6 remain useful regression evidence from the legacy ENA: the new product should not suppress useful model initiative or turn acknowledgement into a stopping point. They are not a reason to create another ENA-specific reasoning framework.

## Current release

The existing Current release remains `v0.3.14 / FIELD_VALIDATION` in the legacy architecture repository: `guytogay/evolution-native-agent-architecture`.
