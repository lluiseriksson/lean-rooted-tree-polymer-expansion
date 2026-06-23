# Release evidence

The release workflow publishes seven primary files sharing the stem
`lean-rooted-tree-polymer-expansion-vX.Y.Z`:

| File | Purpose |
|---|---|
| `.zip` | Deterministic source archive with one top-level directory |
| `.zip.sha256` | Source-archive digest |
| `.spdx.json` | SPDX 2.3 dependency and build-dependency SBOM |
| `.cdx.json` | CycloneDX 1.5 dependency and build-dependency SBOM |
| `.buildinfo.json` | Deterministic record binding the archive, SBOMs, proof pins, and verification commands |
| `.release.json` | Machine-readable release index binding all primary evidence files |
| `.checksums.sha256` | Aggregate SHA-256 list for the ZIP, both SBOMs, build information, and release index |

Each JSON evidence file also has its own `.sha256` sidecar. The release index
records byte lengths and digests, while the build-information record captures
the proof environment and verification policy.

## Local verification

```bash
sha256sum -c lean-rooted-tree-polymer-expansion-vX.Y.Z.checksums.sha256
python3 scripts/verify_release.py \
  release/lean-rooted-tree-polymer-expansion-vX.Y.Z.zip
```

The verifier rejects path traversal, duplicate members, case-insensitive and
Unicode-normalization collisions, symlinks, non-regular entries, encryption,
oversized members, unlisted files, forbidden standalone PDFs, malformed source
manifests, dependency-pin drift, malformed SBOM metadata, and release-index or
build-information digest mismatches.

## Clean-room source test

```bash
make smoke-release
```

This safely extracts the source ZIP into a temporary directory and invokes
`scripts/cleanroom_audit.py`, which reruns the dependency-free tests and source
audits using only the extracted tree.

## GitHub attestation

Tagged releases are accompanied by GitHub build-provenance attestations for the
source archive and evidence set. Verify those attestations against downloaded
artifacts using the GitHub CLI and the repository policy in force at release
time.
