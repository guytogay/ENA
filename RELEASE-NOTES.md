# ENA v2.0.0

ENA v2.0.0 is the first major update to the clean ENA product line. It keeps the same goal—preserve viable agency with runtime capabilities the model cannot get from reasoning alone—but tightens the machine contracts around readiness, recovery, attribution, refusal behavior, and evidence reproducibility.

This is a major release because two persisted-state contracts are intentionally not backward compatible: a v1.0.0-era READY home without verification provenance is no longer accepted as READY, and SAFE-CHANGE `rescue.yaml` moves from schema `0.3` to `0.4` for packages that must arm under the v2 gate. Both migrations are explicit in `UPGRADING.md`.

## What changes

- **Evidence-bearing First Use** — recovery and rescuer facts only satisfy minimum readiness when they carry caller-supplied `SELF_ASSERTED` verification provenance (`verification_evidence` plus an offset-aware `verified_at`). Existing scalars are not silently promoted.
- **Honest cold/incremental adoption** — `ena_first_use.py` can stop at `NOT_READY` without manufacturing authority or pretending an initialized home exists.
- **Material UNKNOWN lifecycle** — facts that materially affect operation can carry an explicit owner, reason, resolution path, revisit time, and last-attempt time in `SYSTEM.yaml` without creating a second state ledger.
- **Stronger SAFE-CHANGE arming** — `rescue.yaml` schema `0.4` requires explicit communication verification, restore scope, fallback/escalation, and declarations about whether one operation touches the only communication or recovery path. The arm-time basis is copied into transition history.
- **Fail-closed initialization** — controlled caller-state refusals use exit `2`; invalid targets are rejected before working directories are created; regular-file `--home` inputs no longer produce tracebacks.
- **Resolved-home diagnostics** — preflight keeps its existing first-line `OK` / `REFRESH REQUIRED` status and now also names the exact resolved home it checked, without scanning for alternate homes.
- **Durable actor attribution** — ENA-written change, validation, candidate, and outcome artifacts carry executor / initiator / channel / correlation attribution when supplied by the Host or A2A bridge.
- **Raw-byte source digests** — Sleep/Dream JSONL `sha256` values now hash the exact source bytes, so `sha256sum`, `Get-FileHash`, and equivalent Host tools reproduce the recorded value. CRLF and UTF-8 BOM differences remain visible in the digest while the parser can still tolerate them.
- **Cross-platform contract coverage** — Ubuntu and Windows regressions cover the strengthened First Use, SAFE-CHANGE, refusal, upgrade, home-boundary, digest, and documentation contracts.

## Upgrading from v1.0.0

Read `UPGRADING.md` before treating a new refusal as a broken environment.

### READY homes

A v1.0.0-era home with `minimum_ready: true` but no recovery/rescuer verification provenance intentionally returns `REFRESH REQUIRED` under v2. Re-check the real recovery path and rescuer, then re-assert both facts through `ena_first_use.py` with durable evidence references. Do not fabricate provenance simply to regain READY.

### SAFE-CHANGE packages

For an existing schema-`0.3` package that must be armed under the v2 gate, reconcile its `rescue.yaml` to `0.4` and explicitly resolve all five new declarations:

- `verify_communication` — concrete two-way check or exact `NOT_NEEDED`;
- `restore_only` — concrete restore scope, with no generic escape token;
- `fallback` — concrete fallback/escalation or exact `NOT_NEEDED`;
- `touches_only_communication_path` — exact `true` or `false`;
- `touches_only_recovery_path` — exact `true` or `false`.

`status.yaml` remains on its own independent schema `0.3`; do not rewrite it merely to make the two version numbers match. See `UPGRADING.md` for the before/after example and migration steps.

### Existing Sleep/Dream bundles

Experimental bundles generated from CRLF or BOM-bearing JSONL under the older text-normalized digest path can contain a digest that does not match the file's raw bytes. Regenerate such bundles when exact byte-level reproducibility matters.

## Evidence boundaries

Real Host use has demonstrated the minimum runtime chain: First Use, recovery verification, a non-trivial SAFE-CHANGE, an evidence-backed outcome, and continuation from persisted state in a genuinely new session. Independent adopter runs have also exercised the strengthened SAFE-CHANGE path and the v2 migration/refusal surfaces.

Those results do **not** turn structural declarations into authenticated proof:

- `verification_evidence` is caller-supplied `SELF_ASSERTED` provenance; ENA checks its presence and shape but does not authenticate arbitrary external evidence or prove the referenced mechanism is currently usable.
- SAFE-CHANGE rescue declarations are self-asserted control facts. Passing the gate proves the required declarations satisfy the machine contract, not that the communication check, restore scope, fallback, or path topology is correct in reality.
- Actor attribution is not authorization.
- A configured A2A reference is not proof of current reachability or capability.
- Reference scripts only enforce what the Host actually routes through them or equivalent Host-native controls.

Sleep/Dream remains **experimental**. Its marginal value over ordinary model reasoning is still **UNMEASURED**. v2.0.0 improves its provenance reproducibility; it does not claim that Dream has been shown to improve outcomes.

## Known boundaries

- `candidate_outcome.py` records evidence references asserted by the operator; it does not verify arbitrary external references or judge evidence sufficiency.
- Sleep/Dream sampling parameters remain experimental field parameters, not normative intelligence settings.
- Multi-process transaction isolation is not claimed for candidate outcome recording.
- Host-native recovery, supervisor, snapshot, validation-hook, and permission mechanisms remain the preferred stronger implementation when available.

Licensed under Apache License 2.0.
