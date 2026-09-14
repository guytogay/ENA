# ENA v2.1.0

ENA v2.1.0 is a backward-compatible minor update to the clean ENA product line. It makes adoption lighter, adds a Host-observed way to account for the durable effects of dispatched Agent work, and closes several documentation and operator-diagnostic gaps found after v2.0.0 shipped.

There is **no required persisted-state migration from v2.0.0 to v2.1.0**. Existing v2.0.0 READY homes and SAFE-CHANGE packages remain valid under the same contracts. If you are upgrading from v1.0.0-era state, the v2 migration rules in `UPGRADING.md` still apply.

## What changes

- **A2A effect receipts** — `tools/ena_peer_effect.py` can snapshot a declared observation scope before dispatched work, observe the same scope afterwards, and record `added` / `removed` / `modified` effects keyed by the same correlation id used for attribution. The initiating side can retrieve a compact receipt instead of treating a child session's narrative `DONE` as proof of durable effect.
- **Effect evidence stays separate from attribution and authorization** — `ENA_PEER_CALLER` / `ENA_PEER_TASK_ID` still answer who initiated the work. The new effect record answers what the Host observed inside the declared scope. The scope is an observation boundary, not an authorization boundary, and the helper never rejects work merely because an effect was unexpected.
- **Incomplete observation fails visibly** — missing or unreadable declared scopes do not produce a false empty result. The tool writes an incomplete record and returns its documented semantic exit code `3` so callers can distinguish a bounded observation with limitations from a complete observation.
- **Symlink-safe, content-based comparison** — directory symlinks are recorded rather than followed, so they cannot silently widen the observation surface, and regular-file modification is decided from content digests rather than timestamps alone.
- **Leaner adoption path** — the mandatory reading path is now four documents: `FIRST-USE.md`, `SURVIVAL.md`, `SAFE-CHANGE.md`, and `EVOLUTION.md`. `A2A.md` and `SLEEP-DREAM-QUICKSTART.md` remain available when those capabilities are actually needed instead of being universal adoption steps.
- **Documentation/interface regression coverage** — CI now checks that documented `tools/*.py` examples refer to shipped tools and valid flags, that the reference-tool inventory matches reality, and that subcommand-based CLIs are checked against the documented subcommand's own help rather than a misleading top-level union.
- **Corrected operator-facing behavior descriptions** — the documented `automatic_rollback` behavior now matches the existing case-insensitive gate instead of implying only lowercase `true` / `false` are accepted.
- **Cleaner preflight diagnostics** — an unparsable `SYSTEM.yaml` is reported once rather than twice with a nested duplicate prefix; the refusal code and fail-closed behavior are unchanged.
- **Post-v2 adopter corrections** — documentation now matches the shipped scaffold markers, SAFE-CHANGE transition behavior, transition-history creation point, legacy migration source, unattended First Use authority, and bare-session recovery evidence found during an independent adoption run.

## A2A effect receipts

Use the effect helper when a Host or bridge can observe the target surface from outside the dispatched child/headless session and durable effect matters.

Before dispatch:

```bash
python tools/ena_peer_effect.py snapshot \
  --scope /path/to/declared/scope \
  --out before.json
```

After the dispatched work exits:

```bash
python tools/ena_peer_effect.py record \
  --before before.json \
  --correlation-id <the same task/correlation id> \
  --out record.json \
  --index records.jsonl
```

The stdout receipt contains only the stable caller-facing minimum: `correlation_id`, `record`, `added_count`, `removed_count`, and `modified_count`. The durable record contains the observed before/after inventory and its own completeness/limitation state.

A child session does not need to cooperate with the recorder. To call the result Host-generated evidence, perform the observation and keep the record outside that child session's writable surface.

## Upgrading from v2.0.0

No migration is required.

- Existing v2.0.0 READY homes remain READY subject to their normal freshness and evidence requirements.
- Existing SAFE-CHANGE schema-`0.4` rescue packages do not need a v2.1 rewrite.
- A2A effect receipts are optional; adopting them does not change the existing actor-attribution contract.
- The shorter mandatory reading path removes universal reading obligations; it does not remove the A2A or Sleep/Dream capabilities from the product.

If the starting point is v1.0.0-era persisted state rather than v2.0.0, follow `UPGRADING.md` for the v2 readiness-provenance and SAFE-CHANGE migration rules before interpreting a refusal as an environment failure.

## Evidence boundaries

The new effect recorder deliberately has a bounded claim:

- a scoped receipt proves what the Host observed inside the declared roots; it does **not** prove the rest of the machine was unchanged;
- the declared scope does not grant permission to modify it and is not an authorization policy;
- effect evidence does not replace actor attribution;
- exit `3` means the record exists but the observation had declared limitations; it must not be treated as a complete zero-effect result;
- Hosts with stronger native filesystem/change-journal mechanisms may use them instead of the reference helper;
- hashing cost grows with the observed scope, so large trees may be better served by Host-native mechanisms.

Reference scripts still enforce only what the Host routes through them or equivalent Host-native controls.

Sleep/Dream remains **experimental**. Its sampling parameters — sizes and weights — remain experimental field parameters, not normative intelligence settings, and passing code and tests are not proof that the mechanism improves decisions. Its marginal value over ordinary model reasoning is still **UNMEASURED**; v2.1.0 does not promote it or claim improved decision quality.

Measured while this release was being prepared: the sampler draws from pools derived from the material's aggregate shape (`recent` / `old` / `underused` / `salient` slices plus a time-ordered list), so a small material change can reshuffle most of a same-seed sample — removing one record, or moving one timestamp, moved 4 of the 6 selected fragments, while rewording a fragment's text moved none. Determinism for identical input holds. Two Dream cycles over a growing material are therefore not directly comparable at a fixed seed, which is one concrete reason the marginal-value question remains open.

Licensed under Apache License 2.0.
