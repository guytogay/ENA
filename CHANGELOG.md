# Changelog

All notable changes to the clean ENA product line are recorded here.

## Unreleased

### Documentation
- Documented what the Dream sampler's two controls actually do, after a field host reported a measured defect (#93) and the maintainer ruling was to clarify rather than change behaviour. `--seed` is a replay/debugging control and should be omitted for recurring live or scheduled runs, where the sampler generates and records a fresh seed; `--count` includes the anchor, so the default `6` leaves at most five slots for six named pools and one pool is omitted, with the omitted pool depending on material and seed; a fixed seed also pins the position drawn inside a pool, which is how new material can be systematically missed when a single pool is its only route. `--count 7` leaves room for the anchor plus all six pools but is a field choice, not a coverage guarantee. Both points are now in the tool's `--help` and in `tools/README.md`, the documented example no longer pins a seed, and `tools/test_dream_sampler_instructions.py` holds the statements and the default in CI.
## 2.1.0 — 2026-09-14

ENA v2.1.0 is a backward-compatible minor release that adds Host-observed A2A effect receipts, reduces the universal adoption path, and fixes post-v2 documentation and operator-diagnostic mismatches. No persisted-state migration is required from v2.0.0.

### Added
- Added `tools/ena_peer_effect.py` and the A2A effect-observation guidance from #88. The optional helper snapshots one or more declared scopes before dispatched work, re-observes them afterwards, derives `added` / `removed` / `modified` from content digests, writes a durable record keyed by the existing correlation id, can append a retrievable JSONL locator, and prints a compact receipt. The scope is an observation boundary rather than an authorization boundary; symlinks are recorded rather than followed; incomplete observations write an explicitly incomplete record and return semantic exit `3` instead of producing a false empty result. This is the deliberate net-growth exception approved for #88.
- Added a narrow documentation/interface regression to CI on Ubuntu and Windows. It verifies that documented `tools/*.py` examples name shipped tools and valid flags, that `tools/README.md` inventories the actual entry points, and that subcommand-based examples are validated against the documented subcommand's own help.
- Pinned the ordered mandatory reading path in CI: `FIRST-USE.md`, `SURVIVAL.md`, `SAFE-CHANGE.md`, `EVOLUTION.md`; `A2A.md` and `SLEEP-DREAM-QUICKSTART.md` must remain conditional capability reading unless a later product decision explicitly changes that contract.

### Fixed
- Corrected `automatic_rollback` documentation to match the shipped case-insensitive behavior. Existing accepted spellings such as `True` and `FALSE` remain accepted; the product does not introduce a new refusal merely to make prose and implementation agree.
- Fixed `ena_preflight.py` so an unparsable `SYSTEM.yaml` is reported once rather than twice with a nested duplicate prefix. Exit `2` and fail-closed behavior are unchanged.
- Corrected adopter-facing documentation after an independent run of the published v2.0.0 artifact: scaffold unresolved markers, `automatic_rollback` / `rollback_mode` behavior, the first successful creation of `transitions.jsonl`, the source and abbreviated shape of legacy upgrade examples, unattended timezone/language authority, and the bare-session archive-plus-rehearsed-restore recovery recipe now match measured product behavior.

### Documentation
- Reduced the mandatory adoption path from six documents to four after an unprimed-reader review found that A2A and experimental Sleep/Dream had become universal reading obligations even though the product itself does not require those capabilities. `A2A.md` and `SLEEP-DREAM-QUICKSTART.md` remain in the product as conditional capability guides.
- Removed duplicated adopter prose and restored single ownership of repeated instructions: First Use commands point to `FIRST-USE.md`, the tool inventory to `tools/README.md`, validation/repair trajectory to `SAFE-CHANGE.md`, and Sleep/Dream experience-selection details to `SLEEP-DREAM.md`.
- Clarified that the CI workflow is the acceptance line for the shipped reference-tool tests, added the worked Git shape promised by `examples/change/SESSION-GIT-WORKTREE.md`, and marked `UPGRADING.md` as unnecessary for first-time adopters.
- Verified the documentation cut against the twenty rules extracted by an unprimed reader: all 20 remained present after the restructuring, so the change removes repetition and misplaced obligations rather than product rules.
## 2.0.0 — 2026-09-13

ENA v2.0.0 strengthens machine-readable readiness, SAFE-CHANGE recovery declarations, controlled-refusal behavior, and evidence reproducibility. This is a major release because previously accepted persisted state can require explicit operator migration before the v2 gates accept it again.

### Added
- Durable five-field actor attribution on ENA-written change, validation, candidate, and outcome artifacts, including A2A initiator/correlation propagation where the Host supplies it (#57).
- Material `UNKNOWN` lifecycle metadata in `SYSTEM.yaml`, with responsibility, revisit, and last-attempt fields for facts that materially affect current operation (#59).
- An executable cold/incremental First Use path that can stop honestly at `NOT_READY` without manufacturing authority or an initialized home (#62).
- Per-fact verification provenance for the minimum recovery path and rescuer: `verification_confidence`, `verification_evidence`, and offset-aware `verified_at` (#66).
- Explicit SAFE-CHANGE declarations for communication verification, restore scope, fallback/escalation, and whether one operation touches the only communication/recovery paths; the armed transition preserves those declarations in history (#71).

### Hardened
- Remaining text-mode subprocess tests now pin UTF-8 decoding instead of depending on the Host locale (#58).
- First Use inspection no longer promotes existing scalars, rewrites READY state, or deletes lifecycle evidence merely because a value is present (#66).
- Minimum readiness now accepts only canonical lowercase `true` and requires evidence-bearing provenance for both minimum facts (#66).
- SAFE-CHANGE `armed` now fails closed while required rescue declarations are unresolved, and refuses an operation declared to touch both the only communication path and the only recovery path (#71).
- `ena_init.py` now treats caller-state rejection as a controlled refusal with exit `2`, while documented tool-specific semantic result codes remain distinct; see `tools/EXIT-CODES.md` (#64).
- Initialization validates the target and existing ENA control files before creating working directories, and a regular-file `--home` now fails cleanly without a traceback or filesystem side effect (#72).
- Sleep/Dream source `sha256` values now hash the exact source-file bytes, so operators can reproduce them with standard Host hashing tools on every platform (#70).
- `ena_preflight.py` now reports the exact resolved home it checked on both `OK` and `REFRESH REQUIRED` paths without scanning for alternate homes or changing home precedence (#67).

### Documentation and adopter surface
- Added `UPGRADING.md` with an explicit v1.0.0-era READY-home migration path rather than treating the strengthened readiness refusal as an environment failure.
- Added an explicit SAFE-CHANGE `rescue.yaml` 0.3 → 0.4 migration path, clarified the independent `status.yaml` / `rescue.yaml` schema versions, the scaffold `UNKNOWN` marker, the five declarations that must all be resolved before arming, and the actual package-name shape (#78).
- Kept the shared reference-tool inventory aligned with the contract-bearing `safe_change_rescue.py` module (#75).

### Breaking / migration
- A home that was `minimum_ready: true` under the v1.0.0-era predicate but lacks recovery/rescuer verification provenance now fails closed as `REFRESH REQUIRED`. This is intentional; the old READY claim is no longer sufficient evidence under the strengthened contract.
- Do **not** fabricate provenance or blindly grandfather old values. Re-check the existing recovery path and rescuer, then re-assert each fact once through `ena_first_use.py` with a durable evidence reference. See `UPGRADING.md` for the exact migration command.
- The machine-readable First Use control format remains readable; the incompatibility is the readiness predicate and required provenance for a READY claim.
- SAFE-CHANGE `rescue.yaml` advances from schema `0.3` to `0.4`. Existing packages that must be armed under v2 tooling must explicitly reconcile `verify_communication`, `restore_only`, `fallback`, `touches_only_communication_path`, and `touches_only_recovery_path`; old packages are not grandfathered. See `UPGRADING.md` for the field-by-field migration (#71, #78).
- Existing experimental Sleep/Dream bundles produced from CRLF or BOM-bearing JSONL inputs may contain the former text-normalized digest; regenerate them when exact source-byte reproducibility matters (#70).

### Evidence boundary
- Recovery/rescuer `verification_evidence` remains caller-supplied `SELF_ASSERTED` provenance. The reference tools enforce presence and shape; they do not authenticate arbitrary external evidence or prove the mechanism is currently usable.
- SAFE-CHANGE rescue declarations are machine-gated self-asserted control facts. Passing the gate does not prove the communication check, restore scope, fallback, or path topology is correct in reality.
- Actor attribution is not authorization.
- Sleep/Dream remains experimental. Its marginal value over ordinary model reasoning is still `UNMEASURED`; v2.0.0 does not claim otherwise.
- Reference scripts only enforce boundaries that the Host actually routes through them or equivalent Host-native controls.

## 1.0.0 — 2026-09-12

First stable clean-product baseline.

### Added
- Minimal First Use with explicit system freshness, recovery, rescuer, and startup preflight.
- SAFE-CHANGE reference tooling with explicit state transitions, prepared recovery, evidence-gated terminal states, and Host-profile-aware recovery semantics.
- Incremental validation events and freshness scanning for evolution evidence.
- Experimental Sleep/Dream reference tools with bounded inputs, provenance, replayable sampling, cross-session/knowledge/capability material, and speculative candidate recording.
- Reality-contact outcome recording for `retain`, `revise`, `reject`, and `restore`, while keeping the judgment outside the recorder.
- A2A guidance that separates configured discovery references from live reachability.
- Repository hygiene checks and protected-main workflow requirements.

### Hardened
- Shared initialized-home and canonical-time boundaries across durable writers.
- Collision-safe candidate output and immutable outcome records.
- UTF-8 BOM tolerance for Host-native Windows write paths.
- Fail-closed freshness metadata parsing and explicit UNKNOWN semantics.
- One authority per fact class between `ENA.yaml` and `SYSTEM.yaml`.
- Relocation-safe ENA path pointers, including moved-home protection against writes to stale absolute paths.
- Cross-platform Ubuntu/Windows regression coverage for the shipped reference tools.

### Evidence boundary
- Real Host work has demonstrated the minimum runtime chain: First Use, recovery verification, non-trivial SAFE-CHANGE, evidence-backed outcome, and continuation in a genuinely new session.
- Sleep/Dream remains experimental. Its marginal value over ordinary model reasoning is still `UNMEASURED`; v1.0.0 does not claim otherwise.
- Reference scripts only enforce boundaries that the Host actually routes through them or equivalent Host-native controls.
