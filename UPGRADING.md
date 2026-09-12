# Upgrading ENA

This file records adopter-visible migrations between released ENA product versions. It is not a second state ledger; the live authorities remain `ENA.yaml` and `SYSTEM.yaml`.

## From v1.0.0-era readiness to the provenance-bearing contract

Current `main` strengthens the First Use minimum beyond the v1.0.0-era READY shape. A home that previously had:

```yaml
minimum_ready: true
recovery:
  primary: SOME_RECOVERY_REFERENCE
rescue:
  primary: SOME_RESCUER_REFERENCE
  type: human
```

but no per-fact verification provenance is intentionally no longer READY. After upgrading, `ena_preflight.py` returns `REFRESH REQUIRED` rather than grandfathering an unverifiable old claim.

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

## Versioning consequence

The persisted-state format remains readable, but the meaning of machine-readable READY is not backward compatible: a home accepted as READY under the v1.0.0-era predicate can be refused under the strengthened predicate until migrated. Under ENA's semantic-version policy, this change requires the next formal release to use a new major version. The current release remains v1.0.0 until a release-preparation change updates `VERSION`, README release line, changelog entry, release notes, and tag together.
