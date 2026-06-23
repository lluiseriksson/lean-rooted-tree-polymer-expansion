# Release evidence

The release directory is an exact 13-file protocol. Six primary files share the
stem `lean-rooted-tree-polymer-expansion-vX.Y.Z`; each has one canonical
`.sha256` sidecar, and one ordered aggregate checksum file covers all six.

| Primary file | Purpose |
|---|---|
| `.zip` | Deterministic source archive with one top-level directory |
| `.spdx.json` | SPDX 2.3 dependency and build-dependency SBOM |
| `.cdx.json` | CycloneDX 1.5 dependency and build-dependency SBOM |
| `.buildinfo.json` | Deterministic record binding the archive, SBOMs, proof pins, and declared verification entrypoints |
| `.intoto.jsonl` | Deterministic, non-execution-bound in-toto/SLSA declaration of subjects, inputs, dependencies, and required external gates |
| `.release.json` | Machine-readable release index binding the five preceding primary artifacts |

The final file is
`lean-rooted-tree-polymer-expansion-vX.Y.Z.checksums.sha256`. It contains the
six primary digests in canonical order. `scripts/release_inventory.py` is the
single source definition for filenames, media types, roles, sidecars, ordering,
and exact-set validation.

No other entry is publishable. Verification rejects missing or unexpected
files, directories, symlinks, non-regular entries, malformed sidecars, duplicate
or reordered checksum rows, uppercase or otherwise non-canonical digests,
incorrect separators, and a missing final LF.

## Local verification

```bash
sha256sum -c lean-rooted-tree-polymer-expansion-vX.Y.Z.checksums.sha256
python3 scripts/verify_release.py \
  release/lean-rooted-tree-polymer-expansion-vX.Y.Z.zip
```

The verifier also rejects path traversal, duplicate archive members,
case-insensitive and Unicode-normalization collisions, symlinks, non-regular ZIP
entries, encryption, oversized members, unlisted source files, forbidden
standalone PDFs, malformed source manifests, dependency-pin drift, malformed
SBOM metadata, provenance-policy drift, and release-index or build-information
digest mismatches. It requires the exact builder identity, source-input digests,
five resolved dependencies, release recipe, external Lean gates, and
non-execution-bound metadata rather than only checking the outer in-toto shape.

## Privilege-separated publication

The tagged workflow first runs `verify-and-package` with read-only repository
permission. That job performs Lean/oracle verification and deterministic
packaging, then uploads the exact `release/` directory as a short-lived workflow
artifact.

A separate tag-only `publish` job receives the write, OIDC, and attestation
permissions. It does not check out the repository and does not execute
repository scripts. An inline dependency-free validator reconstructs the
expected 13 filenames from the semantic-version tag, checks every sidecar and
the aggregate bytes, confirms release-index identity and artifact order, and
only then attests and uploads all paths explicitly. Broad publication globs are
forbidden by the workflow audit.

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
