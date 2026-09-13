# Changelog

All notable changes to the clean ENA product line are recorded here.

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
