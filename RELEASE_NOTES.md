# Release notes: v2.4.3

Version 2.4.3 hardens the final publication boundary. It preserves the exact
three public Lean theorem statements, upstream proof commit, Lean toolchain,
Mathlib commit, oracle axiom boundary, and mathematical claims boundary from
v2.4.2.

## Read-only verification, minimal privileged publication

The tagged release workflow is now split into two jobs. `verify-and-package`
checks out the source, performs the single explicit Lean build, runs
`leanchecker`, audits the exact oracle, and creates the deterministic evidence
set with only `contents: read` permission. It then transfers the already
verified `release/` directory as a short-lived workflow artifact.

A separate tag-only `publish` job receives the write, OIDC, and attestation
permissions. That job does not check out the repository and does not execute any
repository script or generated executable. It only downloads the candidate,
validates its data and filenames with an inline dependency-free check, requests
hosted attestations, and invokes `gh release create`. A manual workflow dispatch
therefore exercises the read-only verification job but cannot publish a release.

## Exact 13-file release protocol

Release publication no longer relies on broad shell globs. The accepted set is
exactly six primary checksum subjects, their six canonical `.sha256` sidecars,
and one aggregate checksum file. The privileged job rejects missing,
unexpected, symlinked, non-regular, misnamed, reordered, or checksum-inconsistent
entries before any attestation or upload. The GitHub release command receives
all 13 paths explicitly, so an aggregate checksum cannot be uploaded twice and
a stale file left in `release/` cannot be published accidentally.

`scripts/release_inventory.py` is now the single local definition of this
protocol. ZIP, SPDX, CycloneDX, build-information, provenance, release-index,
determinism, and verification tooling share its sidecar and aggregate-checksum
implementation. Release verification compares sidecars and the aggregate file
byte for byte, enforcing lowercase SHA-256, the two-space separator, canonical
ordering, and final LF rather than accepting merely parseable checksum text.
It also binds the ordered release-index and build-information records to exact
roles, media types, source sets, proof-environment identity, sizes, and digests.

## Bounded repository scans

Source inventory and artifact audits now prune `.git`, `.lake`, generated site,
release, cache, and virtual-environment directories before filesystem descent.
The artifact audit reuses the already validated canonical source inventory
instead of performing two additional recursive walks. This keeps local checks
fast after documentation dependencies have been installed without weakening
symlink, non-regular-file, portable-name, or manifest-drift detection.

## Regression policy

The workflow audit now requires privilege separation, read-only default
permissions, a tag-only publisher, immutable upload/download actions, no source
checkout or repository-script execution in the privileged job, exact asset
paths, and token scoping to the final publication step. Focused tests cover
workflow-wide write permission, wildcard publication, privileged source
checkout, privileged repository-script execution, unexpected assets,
non-canonical sidecars, reordered aggregate checksums, and non-regular release
entries.

## Mathematical scope

The release formalizes finite rooted-tree and target-sensitive second-Ursell
bounds. It does not prove the model-specific raw Yang--Mills activity estimate,
`hRpoly`, a continuum construction, Osterwalder--Schrader reconstruction, or a
mass gap theorem.
