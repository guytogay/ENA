# ENA v2.1.1

ENA v2.1.1 is a **patch release**: it carries corrected documentation and CLI help text for the Dream sampler's two controls. **No behaviour changes, no new contract surface, and no persisted-state migration.** The tool, its defaults, and its exit codes are exactly those of v2.1.0.

It exists because of how adoption works: the clarification was written after a maintainer ruling on a field report, but it landed on `main` one commit *after* the v2.1.0 tag. A host that pins release tags for reproducibility therefore received the pre-ruling wording — describing `--seed` as a bare parameter with no note that a fixed seed pins the sampling positions. Shipping the same text inside a tag is the point of this release; nothing else changed.

## What changes

- **`--seed` is a replay/debugging control.** Recurring live or scheduled runs should omit it; the sampler then generates a fresh seed and records it in the run record, so the run stays reproducible after the fact. A **fixed** seed also pins *which* pool is omitted and *which position* is drawn inside a pool, which is how new material can be systematically missed when a single pool is its only route into the sample.
- **`--count` includes the anchor.** The default `6` therefore leaves at most five slots for six named pools and one pool is omitted; `--count 7` leaves room for the anchor plus all six pools, but that is a field choice rather than a coverage guarantee.
- **Both statements are now enforced, not just written.** They live in the tool's `--help`, in `tools/README.md`, the documented example no longer pins a seed, and `tools/test_dream_sampler_instructions.py` holds the statements and the default in CI, so the documentation cannot drift away from the tool silently.

## Upgrading from v2.1.0

No migration is required, and no action is required beyond reading the corrected text.

- Existing READY homes, SAFE-CHANGE packages and A2A effect records are unaffected.
- If a scheduled or recurring run passes an explicit `--seed`, that is now documented as the wrong usage; omitting it is the documented behaviour. Changing it is optional and reversible.
- If a run uses `--count 6` while relying on all six pools being sampled, the documentation now says plainly that one pool is omitted each round.

## Evidence boundaries

The clarification came from a field host's measured report, and the measurement did not decide behaviour:

- the maintainer ruling was to **document rather than change** the sampler, so v2.1.1 contains no behavioural fix;
- the reported mechanism was reproduced independently before the wording was written, and the wording was corrected where the original report generalised too far (the omitted pool is fixed *by material and seed*, not permanently one named pool);
- the new CI test asserts the documented statements and the default, not the sampling quality.

Sleep/Dream remains **experimental**. Its sampling parameters — sizes and weights — remain experimental field parameters, not normative intelligence settings, and passing code and tests are not proof that the mechanism improves decisions. Its marginal value over ordinary model reasoning is still **UNMEASURED**; v2.1.1 does not promote it or claim improved decision quality.

Measured while v2.1.0 was being prepared, and still true: the sampler draws from pools derived from the material's aggregate shape (`recent` / `old` / `underused` / `salient` slices plus a time-ordered list), so a small material change can reshuffle most of a same-seed sample — removing one record, or moving one timestamp, moved 4 of the 6 selected fragments, while rewording a fragment's text moved none. Determinism for identical input holds. Two Dream cycles over a growing material are therefore not directly comparable at a fixed seed, which is one concrete reason the marginal-value question remains open.

Licensed under Apache License 2.0.
