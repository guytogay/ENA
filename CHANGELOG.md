# Changelog

All notable changes to the clean ENA product line are recorded here.

## Unreleased

This unreleased line contains a breaking persisted-state readiness change. Under ENA's semantic-version policy it must not be released as `1.0.x` or `1.1.x`; the next release target is **2.0.0**.

### Added
- Durable five-field actor attribution on ENA-written change, validation, candidate, and outcome artifacts, including A2A initiator/correlation propagation where the Host supplies it (#57).
- Material `UNKNOWN` lifecycle metadata in `SYSTEM.yaml`, with responsibility, revisit, and last-attempt fields for facts that materially affect current operation (#59).
- An executable cold/incremental First Use path that can stop honestly at `NOT_READY` without manufacturing authority or an initialized home (#62).
- Per-fact verification provenance for the minimum recovery path and rescuer: `verification_confidence`, `verification_evidence`, and offset-aware `verified_at` (#66).

### Hardened
- Remaining text-mode subprocess tests now pin UTF-8 decoding instead of depending on the Host locale (#58).
- First Use inspection no longer promotes existing scalars, rewrites READY state, or deletes lifecycle evidence merely because a value is present (#66).
- Minimum readiness now accepts only canonical lowercase `true` and requires evidence-bearing provenance for both minimum facts (#66).

### Breaking / migration
- A home that was `minimum_ready: true` under the v1.0.0-era predicate but lacks recovery/rescuer verification provenance now fails closed as `REFRESH REQUIRED`. This is intentional; the old READY claim is no longer sufficient evidence under the strengthened contract.
- Do **not** fabricate provenance or blindly grandfather old values. Re-check the existing recovery path and rescuer, then re-assert each fact once through `ena_first_use.py` with a durable evidence reference. See `FIRST-USE.md` for the exact migration command.
- The machine-readable control format remains readable; the incompatibility is the readiness predicate and required provenance for a READY claim.

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
