# Changelog

All notable changes to the clean ENA product line are recorded here.

## Unreleased

### Documentation
- Cut the mandatory reading path from six documents to four (6,791 → 5,390 words, −21%) after a deletion review whose unprimed reader found that the entry path required two capabilities the product itself declines to require. `A2A.md` (whose own text says A2A is not a universal installation gate, and which a fresh reader could not turn into a next action) and `SLEEP-DREAM-QUICKSTART.md` (an experimental mechanism whose value every other surface calls unmeasured) moved from "read and apply these in order" to a "read when a capability needs it" list. Nothing was removed from the product.
- Removed the duplicated material the review identified: the README's First Use command blocks and tool inventory now point at `FIRST-USE.md` and `tools/README.md`; the validation/repair trajectory has one owner (`SAFE-CHANGE.md`) instead of three; `SLEEP-DREAM-QUICKSTART.md` §4 points at `SLEEP-DREAM.md` §3 for what experience is worth keeping; `A2A.md` lost a redundant two-line configuration example and a repeated credentials warning; `SURVIVAL.md`'s recovery bullet was split so a rule is no longer buried in a wall of prose.
- Two reader-blocking gaps closed: `tools/README.md` now states that the CI workflow is the acceptance line (its earlier list of nineteen tests sat beside the README's six with neither labelled authoritative), and `examples/change/SESSION-GIT-WORKTREE.md` now carries the worked Git shape it is named after instead of deferring every command to the reader's own repository knowledge. `UPGRADING.md` states up front that a first-time adopter should skip it.
- Verified with a rule-preservation probe: the twenty rules an unprimed reader distilled from the adopter path are present before and after the restructuring (20/20), so the cut removed repetition rather than rules.

### Fixed
- Corrected a documentation/behaviour mismatch on `automatic_rollback`: `tools/README.md` and the `safe_change_state.py` docstring both said the field "accepts exactly `true` or `false`", but the comparison has always been case-insensitive, so `True` and `FALSE` arm normally. The wrong wording invited a later "fix" that would have started refusing declarations adopters already use. The accepted spellings are now asserted by a test, and both texts state the behaviour and list what actually blocks (`flase`, `maybe`, `yes`, `1`).
- `ena_preflight.py` no longer prints an unparsable `SYSTEM.yaml` twice, and no longer nests the message inside a second copy of its own prefix. Two checks read the same control file (`require_initialized_home` and the dedicated `SYSTEM.yaml` check), so the same failure was reported by both, and the second report re-wrapped an exception that already named the file. The problem list now collapses repeated lines while preserving order. Exit codes, artifacts and documented contracts are unchanged; only the operator-facing diagnostic is corrected.

### Added
- One assertion in `tools/test_doc_interface_surface.py` pinning the entry path cut above: the README's ordered mandatory list must stay exactly `FIRST-USE.md`, `SURVIVAL.md`, `SAFE-CHANGE.md`, `EVOLUTION.md`, and `A2A.md` / `SLEEP-DREAM-QUICKSTART.md` must stay in the conditional "read when a capability needs it" list. Without it, moving either experimental surface back into the install path would silently re-create the contradiction the cut removed. Teeth checked by five sabotages of `README.md` (promote either document, reorder, shorten the list, drop a conditional entry) — all five fail the test.
- `tools/test_doc_interface_surface.py`, a narrow documentation/interface regression guarded in CI on both platforms: every documented `python ... tools/<tool>.py` example must name a tool that ships and pass only flags that tool's own `--help` accepts, the reference-tool inventory in `tools/README.md` must list every entry point that actually ships and nothing that is absent, and literal `tools/<module>.py` references in adopter-facing prose must resolve to a real file. It reads only literal `tools/` paths, so a package-local name such as `rollback.py` is not reinterpreted as a tool path, and it executes nothing but `--help`.

### Documentation
- Corrected adopter-facing documentation after an independent post-release run on the published v2.0.0 artifact (#80): the scaffold's unresolved marker is `null` for `automatic_rollback` / `automatic_rollback_reference` rather than `UNKNOWN`; the `automatic_rollback` field description now matches measured gate and transition behaviour (including `rollback_mode: not_declared` when a configured `rollback.py` arms without a declaration); `transitions.jsonl` is annotated as created by the first gate transition; `UPGRADING.md` states where a `0.3` package comes from and that the legacy READY-home fragment is abbreviated; `FIRST-USE.md` states who may confirm timezone/language when no human is present; `SURVIVAL.md` records the bare-session-host recovery recipe (archive plus rehearsed restore as the evidence).

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
