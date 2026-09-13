# Upgrading ENA

This file records adopter-visible migrations between released ENA product versions. It is not a second state ledger; the live authorities remain `ENA.yaml` and `SYSTEM.yaml`.

ENA v2.0.0 has two deliberate breaking migrations from the v1.0.0 product line:

1. a v1.0.0-era READY home must carry explicit recovery/rescuer verification provenance before v2 accepts it as READY;
2. a SAFE-CHANGE package using `rescue.yaml` schema `0.3` must reconcile the v2 rescue declarations before it can arm under the v2 gate.

Do not treat either refusal as permission to invent data or overwrite live state. Re-contact reality, record the missing basis, and let the normal gate decide.

## From v1.0.0-era readiness to the provenance-bearing contract

ENA v2.0.0 strengthens the First Use minimum beyond the v1.0.0-era READY shape. A home that previously had:

```yaml
minimum_ready: true
recovery:
  primary: SOME_RECOVERY_REFERENCE
rescue:
  primary: SOME_RESCUER_REFERENCE
  type: human
```

but no per-fact verification provenance is intentionally no longer READY. The fragment above is abbreviated and the fields it names are not all top-level: a real v1.0.0-era home also carried `checked_at` and `valid_until` at the top level, `host_profile` under `runtime:`, an `unknowns` value that is an inline empty list in this shape, and the remaining `runtime` / `communication` / `memory` / `change_surfaces` sections. The migration does not depend on reproducing that whole file - only on re-asserting the two minimum facts with evidence. If you want to rehearse the diagnostic on a real file rather than a fragment, that release's own `ena_init.py --verified-minimum` produces one. After upgrading, `ena_preflight.py` returns `REFRESH REQUIRED` rather than grandfathering an unverifiable old claim.

This does **not** mean the recovery path or rescuer suddenly stopped working. It means the newer contract requires the basis of the READY claim to be recorded explicitly.

### Migration

Re-check the real recovery path and rescuer against current reality, then re-assert both facts once with durable evidence references:

```bash
python tools/ena_first_use.py --home ~/.ena \
  --verified-recovery "REAL_RECOVERY_REFERENCE" \
  --recovery-evidence "DURABLE_RECOVERY_CHECK_REFERENCE" \
  --verified-rescuer "REAL_RESCUER_REFERENCE" \
  --rescuer-evidence "DURABLE_RESCUER_CHECK_REFERENCE" \
  --rescuer-type human

python tools/ena_preflight.py --home ~/.ena
```

Use `--rescuer-type agent` or `host` when that is the verified rescuer type.

A successful migration records, beside each minimum fact:

```yaml
verification_confidence: SELF_ASSERTED
verification_evidence: DURABLE_EVIDENCE_REFERENCE
verified_at: OFFSET_AWARE_TIMESTAMP
```

`SELF_ASSERTED` remains a claim boundary. ENA requires the evidence declaration and timestamp shape; it does not independently authenticate an arbitrary external recovery mechanism or rescuer.

Do not invent evidence merely to restore READY, and do not copy an old primary value forward without re-checking it. If the mechanism is no longer usable, leave the home NOT_READY and establish a real replacement instead.

### Diagnostic

The reference gate recognizes the exact old READY shape when both minimum facts and rescuer type are present, `minimum_ready: true`, and all six provenance fields are absent. It reports that the home is a pre-provenance READY home and points to re-verification/re-assertion instead of presenting six unrelated-looking missing-field errors.

Partial or malformed provenance is **not** labeled as a legacy migration case; the ordinary field-specific validation errors remain visible.

## From SAFE-CHANGE `rescue.yaml` 0.3 to 0.4

ENA v2.0.0 strengthens the arm-time recovery contract. A `preparing` package created under the older `rescue.yaml` schema `0.3` is not grandfathered into the v2 gate.

A `0.3` package is one whose `rescue.yaml` was created by v1.0.0-era tooling. The v2 `tools/change_scaffold.py` writes `rescue.yaml` at `0.4` only - it cannot produce the "before" shape for you - while the `status.yaml` of the very same package stays on its own independent `0.3` schema (see above). The before/after example below is deliberately simplified: a real v1.0.0-era `rescue.yaml` also carries `verify_communication`, `restore_only` and `fallback` (all `UNKNOWN` in that release), and the only fields genuinely new in `0.4` are `touches_only_communication_path` and `touches_only_recovery_path`. A v1.0.0 checkout (`git archive v1.0.0` or a clone at that tag) can generate a real `0.3` package if you want to rehearse the migration on a package rather than on a live change.

The migration happens **inside that package's `rescue.yaml`**. Do not create a second package merely to make the version number look current, do not rewrite `transitions.jsonl`, and do not edit `status.yaml` to fake a migration.

`rescue.yaml` and `status.yaml` have independent schemas. In v2 the reference scaffold intentionally emits:

```yaml
# rescue.yaml
schema_version: '0.4'

# status.yaml
schema_version: '0.3'
```

`status.yaml: 0.3` is therefore not evidence that the package is stale. Only the rescue contract moved to `0.4` in this release.

### What changed

Schema `0.4` adds five declarations that the `preparing -> armed` gate consumes:

```text
verify_communication                 concrete two-way check, or exact NOT_NEEDED
restore_only                         exact restore scope; always concrete
fallback                             concrete fallback/escalation, or exact NOT_NEEDED
touches_only_communication_path      exact true or false
touches_only_recovery_path           exact true or false
```

All five must be resolved before arming. Setting one allowed `NOT_NEEDED` token does not make the remaining scaffolded fields optional.

The scaffold uses literal `UNKNOWN` to mean unresolved. The shipped `examples/change/RESCUE.example.yaml` uses readable `REPLACE_WITH_REAL_*` placeholders for exposition; those are instructions to the adopter, not evidence that a real recovery fact has been established.

`verify_communication` and `fallback` accept the exact ENA control token `NOT_NEEDED` when that is genuinely the correct declaration. `restore_only` has no generic escape token because every recovery action has a scope. The two `touches_only_*` fields must be exact YAML booleans `true` or `false`; if both are `true`, the gate refuses arming rather than accepting an exception string.

### Before and after

A simplified older package may contain:

```yaml
schema_version: '0.3'
host_profile: session
target: REAL_TARGET
recovery_actor: REAL_RESCUER
where_to_act: REAL_LOCATION
changed: REAL_CHANGE
known_good: REAL_KNOWN_GOOD
rollback_action: REAL_ROLLBACK
automatic_rollback: false
automatic_rollback_reference: null
restart_or_new_session: REAL_RESTART_PATH
verify_operation: REAL_OPERATION_CHECK
```

After re-checking the change/recovery reality, reconcile the same package's `rescue.yaml` to:

```yaml
schema_version: '0.4'
host_profile: session
target: REAL_TARGET
recovery_actor: REAL_RESCUER
where_to_act: REAL_LOCATION
changed: REAL_CHANGE
known_good: REAL_KNOWN_GOOD
rollback_action: REAL_ROLLBACK
automatic_rollback: false
automatic_rollback_reference: null
restart_or_new_session: REAL_RESTART_PATH
verify_operation: REAL_OPERATION_CHECK
verify_communication: NOT_NEEDED
restore_only: REAL_RESTORE_SCOPE
fallback: NOT_NEEDED
touches_only_communication_path: false
touches_only_recovery_path: false
```

Those values are examples of **shape**, not defaults. In particular, do not copy `NOT_NEEDED` or `false` unless they are true for the actual Host/change surface.

Then ask the normal gate to evaluate the reconciled package:

```bash
python tools/safe_change_state.py CHANGE_PACKAGE armed
```

If it still returns `BLOCKED`, resolve the reported facts instead of editing the state file around the gate.

Historical terminal packages do not need to be cosmetically rewritten merely because v2 exists. The migration is for a package whose recovery contract must be consumed by the v2 arm-time gate.

## Sleep/Dream source digest compatibility

v2 records the generic JSONL `sha256` over the exact source-file bytes. Older experimental bundles generated from CRLF or UTF-8-BOM-bearing inputs may contain the previous text-normalized digest instead.

The old bundle is not retroactively changed. When exact byte-level reproducibility matters, regenerate the experimental bundle from the source under v2 and verify the recorded digest with the Host's normal SHA-256 tool.

## Versioning consequence

The persisted-state files remain readable, but the READY predicate and SAFE-CHANGE arm-time rescue contract are not backward compatible with every state accepted by v1.0.0. That is why this release is v2.0.0 rather than a patch or minor release.
