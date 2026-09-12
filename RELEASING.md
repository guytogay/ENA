# Releasing ENA

ENA releases are named with semantic-version tags such as `v1.0.0`. The repository `VERSION` file stores the same version without the `v` prefix.

## Between releases

Do not let adopter-visible changes accumulate only in Git history.

- After a release, record each adopter-visible product or contract change under `## Unreleased` in `CHANGELOG.md` as it lands.
- If a change makes a previously accepted CLI invocation, machine-readable claim, or persisted ENA home fail under the new contract, classify the SemVer impact before the next release and document the operator migration path before treating the change as release-ready.
- A cheap migration does not make an incompatible contract backward compatible. If a previously accepted public machine contract requires operator migration to become accepted again, treat it as a breaking change unless the affected surface was explicitly experimental/non-public.
- Do not advance `VERSION` or the README release line merely because `main` contains unreleased work. Those identify the last formal release until a release-preparation change reconciles all release surfaces together.

Some release-impact judgments require adopter-context review and cannot be inferred safely from a generic diff. Prefer an explicit migration note over a brittle heuristic that guesses compatibility from field names or file counts.

## Release gate

Before creating a tag or GitHub Release:

1. `VERSION`, the README release line, the changelog entry, and the proposed tag agree exactly.
2. All repository reference-tool tests and `self_test.py` pass on both required CI platforms: Ubuntu and Windows.
3. The cross-tool ENA-home boundary matrix passes for uninitialized, malformed-ENA, malformed-SYSTEM, and healthy homes with no durable writes in invalid states.
4. Path-authority/relocation regressions pass, including the moved-home no-write-back case.
5. Every retained machine-format example matches the actual artifact/tool contract and is discoverable from adopter-facing documentation.
6. No open issue explicitly classified by the maintainer as release-blocking remains unresolved.
7. Release notes preserve evidence boundaries: experimental mechanisms are not described as proven merely because their code/tests pass.
8. `CHANGELOG.md` has no unresolved `Unreleased` migration/version ambiguity: all adopter-visible changes since the previous tag are assigned to the release being cut, and every breaking persisted-state/CLI change has an explicit migration note.

## Mechanical release steps

After the release-preparation PR is merged and the final release gate passes:

1. Tag the exact merged commit as `v<contents of VERSION>`.
2. Create the GitHub Release from that exact tag using `RELEASE-NOTES.md` as the release-note text.
3. Re-check that `VERSION`, tag, README release line, and `CHANGELOG.md` all identify the same version.

Do not tag an earlier validation head when the release-preparation merge changes files after that validation. The tag identifies the exact released tree.

## Evidence-reference boundary

`candidate_outcome.py` records `evidence_refs` as operator-supplied references. It requires them to be non-empty/resolved as declarations, but does not verify that an arbitrary external reference exists or that the cited evidence is sufficient. That distinction is deliberate; structural/sufficiency judgment remains outside the recorder unless a future typed resolver is added.
