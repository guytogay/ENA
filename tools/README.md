# Reference tools

These scripts use only the Python standard library. An Agent can run them as examples and replace them with stronger Host-native mechanisms later.

```text
ena_init.py                 create ENA.yaml, SYSTEM.yaml and working directories
ena_preflight.py            fail fast when First Use is missing/not ready/stale
change_scaffold.py          create a timestamped safe-change package skeleton
safe_change_state.py        gate SAFE-CHANGE state transitions and evidence
validate_change.py          run one deterministic check and record PASS/FAIL experience
freshness_scan.py           report fresh/stale/unknown JSONL records from explicit metadata
sleep_prepare.py            build a bounded Sleep input bundle from JSONL records
combine_dream_material.py   combine memory + knowledge + capability material
dream_sample.py             sample a Dream set with biased randomness / distance
candidate_record.py         write new candidates only into the speculative path
self_test.py                verify the reference tools against included sample data
```

`control_yaml.py` is a shared strict reader used by the control-file tools. It intentionally supports only ENA's mapping/scalar control subset and fails closed on unsupported YAML features such as sequences and multiline scalars.

## Verify the tools

```bash
python tools/test_control_yaml.py
python tools/self_test.py
```

Expected final output:

```text
ENA reference tools: OK
```

## Initialize interactively or from policy

When values are being confirmed during First Use:

```text
python tools/ena_init.py --timezone CONFIRMED_IANA_TIMEZONE --language CONFIRMED_LANGUAGE_TAG
```

This creates `SYSTEM.yaml` with `minimum_ready: false`. Verify a real recovery path and rescuer before marking it ready.

For a trusted deployment/workspace policy that already verified the minimum, the same tool can initialize non-interactively:

```text
python tools/ena_init.py \
  --timezone CONFIRMED_IANA_TIMEZONE \
  --language CONFIRMED_LANGUAGE_TAG \
  --host-profile session \
  --recovery VERIFIED_RECOVERY_REFERENCE \
  --rescuer VERIFIED_RESCUER_REFERENCE \
  --rescuer-type human \
  --verified-minimum
```

`--verified-minimum` is not automatic proof. The caller is asserting that the supplied recovery path and rescuer were actually verified. Missing policy values should remain unresolved rather than being filled with product defaults.

## Preflight at session/startup time

```bash
python tools/ena_preflight.py
```

Configure the Host to run this before ordinary Agent work when a startup/session hook exists. Exit code `2` means First Use must be completed/refreshed before continuing.

## Create and arm a safe-change package

Choose the Host profile from `SAFE-CHANGE.md`:

```text
python tools/change_scaffold.py --name fix-config --timezone CONFIRMED_IANA_TIMEZONE --profile session
```

or use `--profile resident` for a long-running service/daemon style Agent.

The scaffold does not edit live state. It creates flat machine-readable `status.yaml` / `rescue.yaml`, a `change.md`, backup directory, and an intentionally non-working `rollback.py` placeholder. Replace the placeholder or record a verified Host-native recovery action before arming.

After filling the real recovery facts, use the state gate:

```text
python tools/safe_change_state.py CHANGE_PACKAGE armed
python tools/safe_change_state.py CHANGE_PACKAGE applied
```

A blocked `armed` transition returns exit code `2`; do not apply the live change. After the final real check:

```text
python tools/safe_change_state.py CHANGE_PACKAGE retained --evidence VALIDATION_EVENT_OR_RESULT_REF
```

The gate requires evidence for `retained`, `restored`, and `failed`, and writes transition history to `transitions.jsonl`.

This is reference enforcement, not magical interception. A Host must actually route state transitions through this tool (or an equivalent native hook/permission boundary) for the gate to prevent bypass.

For a directly usable session/coding example based on Git branch + worktree + revert, see:

```text
examples/change/SESSION-GIT-WORKTREE.md
```

## Validate immediately after a bounded change

Use a deterministic check the Host already trusts. For example:

```bash
python tools/validate_change.py \
  --name python-compile \
  --target tools/example.py \
  -- python -m py_compile tools/example.py
```

The wrapper returns the check command's exit status and appends a compact event to:

```text
~/.ena/evolution/experience/validation-events.jsonl
```

If a repair follows a failed validation, link the next run with:

```text
--repair-of PRIOR_VALIDATION_EVENT_ID
```

This is intended for PostToolUse, Git, IDE, CI or equivalent Host hooks as well as manual checks. Do not pass secrets on the command line merely to make the record self-contained. Raw stdout/stderr is not persisted unless `--include-output` is explicitly used.

## Report stale knowledge/capability records

When JSONL records carry `checked_at` and `valid_until`, scan them without inventing a product-wide TTL:

```bash
python tools/freshness_scan.py \
  --input examples/evolution/FRESHNESS.example.jsonl \
  --output freshness-report.json
```

Records without an explicit freshness policy are reported as `unknown`. A caller may supply `--max-age-hours` as local policy when `checked_at` exists but `valid_until` does not. Use `--fail-on-stale` only when the surrounding workflow really should stop on stale records.

## Prepare a Sleep input bundle

```bash
python tools/sleep_prepare.py \
  --experience examples/evolution/EXPERIENCE.example.jsonl \
  --memory examples/evolution/MEMORY.example.jsonl \
  --output sleep-input.json
```

Validation/repair events are also useful Sleep material. `examples/evolution/VALIDATION-TRAJECTORY.example.jsonl` shows the minimal shape.

## Combine Dream material from multiple sources

`dream_sample.py` accepts one JSONL stream. Use the combiner when the Dream should include authorized knowledge-base material and the Agent's capability surface as well as memory/session history:

```bash
python tools/combine_dream_material.py \
  --memory examples/evolution/MEMORY.example.jsonl \
  --knowledge examples/evolution/KNOWLEDGE.example.jsonl \
  --capabilities examples/evolution/CAPABILITIES.example.jsonl \
  --output dream-material.jsonl
```

Capability records should preserve whether the capability is actually installed/verified, merely advertised by an Agent Card, or only discoverable but not enabled. Do not convert an advertised or catalog capability into a real ability merely by including it in Dream material.

## Sample a free Dream

```bash
python tools/dream_sample.py \
  --memory dream-material.jsonl \
  --output dream-set.json \
  --seed 42
```

## Sample a problem-guided Dream

```bash
python tools/dream_sample.py \
  --memory dream-material.jsonl \
  --mode problem-guided \
  --anchor-id m4 \
  --output dream-set.json \
  --seed 42
```

The reference sampler's counts/weights are experimental field defaults, not ENA requirements.

## Record a speculative candidate

```text
python tools/candidate_record.py --origin dream --candidate "IDEA" --reality-check "CHECK"
```

The helper always writes to `~/.ena/evolution/candidates/speculative/` and sets `truth_status: speculative`. Generated claims remain separate from factual memory until reality contact produces evidence.
