# Release evidence

The release workflow publishes eight primary files sharing the stem
`lean-rooted-tree-polymer-expansion-vX.Y.Z`:

| File | Purpose |
|---|---|
| `.zip` | Deterministic source archive with one top-level directory |
| `.zip.sha256` | Source-archive digest |
| `.spdx.json` | SPDX 2.3 dependency and build-dependency SBOM |
| `.cdx.json` | CycloneDX 1.5 dependency and build-dependency SBOM |
| `.buildinfo.json` | Deterministic record binding the archive, SBOMs, proof pins, and declared verification entrypoints |
| `.intoto.jsonl` | Deterministic, non-execution-bound in-toto/SLSA declaration of subjects, inputs, dependencies, and required external gates |
| `.release.json` | Machine-readable release index binding all primary evidence files |
| `.checksums.sha256` | Aggregate SHA-256 list for the ZIP, both SBOMs, build information, in-toto declaration, and release index |

Each JSON evidence file also has its own `.sha256` sidecar. The release index
records byte lengths and digests, while the build-information record captures
the proof environment and declared verification policy. The deterministic `.intoto.jsonl` statement is indexed and checksummed with
the rest of the evidence set.

## Local verification

```bash
sha256sum -c lean-rooted-tree-polymer-expansion-vX.Y.Z.checksums.sha256
python3 scripts/verify_release.py \
  release/lean-rooted-tree-polymer-expansion-vX.Y.Z.zip
```

The verifier rejects path traversal, duplicate members, case-insensitive and
Unicode-normalization collisions, symlinks, non-regular entries, encryption,
oversized members, unlisted files, forbidden standalone PDFs, malformed source
manifests, dependency-pin drift, malformed SBOM metadata, provenance-policy
drift, and release-index or build-information digest mismatches. The verifier
requires the exact builder identity, source-input digests, five resolved
dependencies, release recipe, external Lean gates, and non-execution-bound
metadata rather than only checking the outer in-toto shape.

## Clean-room source test

```bash
make smoke-release
```

This safely extracts the source ZIP into a temporary directory and invokes
`scripts/cleanroom_audit.py`, which reruns the dependency-free tests and source
audits using only the extracted tree. The command is process-group supervised,
so timeout or parent loss cannot leave audit descendants running.

## Provenance layers

The deterministic in-toto statement is a reproducible declaration of subjects,
source inputs, resolved dependencies, the release recipe, and required external
Lean gates. It explicitly records `executionBound: false` and
`hostedAttestationRequired: true`; it must not be read as proof that a particular
runner executed.

Tagged releases are separately accompanied by GitHub build-provenance
attestations for the source archive and evidence set. Those hosted attestations
are the execution-bound layer. Verify them against downloaded artifacts using
the GitHub CLI and the repository policy in force at release time.
