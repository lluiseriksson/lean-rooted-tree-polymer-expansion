# Supply-chain and release integrity

The artifact uses complementary integrity layers.

1. **Immutable proof dependency.** `lakefile.lean`, `lake-manifest.json`, and
   `archive/UPSTREAM.lock` agree on exact upstream and Mathlib revisions.
2. **Pinned proof-source blobs.** The two upstream files containing the public
   proofs are recorded by Git blob object ID in the theorem manifest and lock.
3. **Kernel verification.** CI compiles the public wrappers and requires the
   exact documented oracle axiom set for every theorem.
4. **Statement fingerprints.** Whitespace-normalized public Lean declarations
   are SHA-256 fingerprinted, so binder or conclusion drift cannot hide behind
   stable theorem names.
5. **Build-action inventory.** `archive/actions-manifest.json` records every
   external GitHub Action at a full immutable commit SHA, together with the
   audited major-tag label from which it was resolved. Mutable or unlisted
   action refs fail the workflow audit.
6. **Pinned container bootstrap.** The Dockerfile fetches the elan installer
   from a fixed commit and verifies its Git blob object ID before execution.
7. **Audited source-tree manifest.** `MANIFEST.sha256` records every packaged
   source file other than itself. Static and clean-room checks compare the
   committed bytes with the current tree; manifest generation and ZIP assembly
   use the same path-safe source inventory.
8. **Deterministic archive.** ZIP timestamps, permissions, ordering, and root
   directory are normalized; CI requires two independent builds to match
   byte-for-byte.
9. **Archive safety.** Verification rejects traversal, duplicate or
   non-canonical paths, file/directory conflicts, case-folding and Unicode
   collisions, Windows-reserved components, symlinks, non-regular entries,
   encryption, oversized members, unexpected roots, unlisted members, and
   forbidden manuscript binaries.
10. **Canonical release inventory.** `scripts/release_inventory.py` defines
    exactly six primary artifacts, six sidecars, and one aggregate checksum.
    Missing, extra, symlinked, non-regular, reordered, or byte-noncanonical
    entries fail before publication.
11. **Checksums and release index.** Per-file sidecars, an ordered aggregate
    checksum file, and a machine-readable release index bind the complete
    evidence set.
12. **Dual software bills of materials.** Packaging emits SPDX 2.3 and
    CycloneDX 1.5 JSON for locked Lean packages, pinned documentation
    dependencies, and GitHub Actions build dependencies.
13. **Build-information binding.** Deterministic JSON records the proof
    environment, declared verification entrypoints, and archive/SBOM digests.
14. **Supervised process lifecycle.** Local Lean, clean-room, and deterministic
    evidence subprocesses run in isolated process groups and are terminated as
    a complete tree on timeout, interrupt, or parent loss.
15. **Clean-room archive test.** The ZIP is safely extracted into a temporary
    directory and audited using only its own source tree.
16. **Scheduled cold-cache verification.** A monthly workflow rebuilds Lean
    without the GitHub Lean cache and recreates the release evidence.
17. **Privilege-separated publication.** Source checkout, Lean, tests, and
    packaging run with read-only permission. A distinct tag-only job receives
    write and OIDC permissions, executes no repository code, validates the
    transferred candidate, and publishes explicit paths without globs.
18. **Hosted provenance.** Tagged releases request GitHub build-provenance
    attestations for the source archive and JSON evidence files only after the
    exact asset set has passed the privileged-job validator.

GitHub Actions and Python documentation packages are monitored by Dependabot.
The action policy uses full immutable commit SHAs. Dependabot may propose
updates, but a change is accepted only when workflow files, action manifest,
SBOMs, and review evidence move together.

## Python dependency lock

The four direct documentation dependencies are declared in
`requirements-docs.txt`; the exact transitive environment is committed in
`requirements-docs.lock`. Every environment installs the lock. SBOMs enumerate
all locked packages and distinguish direct from transitive scope. The audit
explicitly rejects the obsolete `cffconvert` and minifier package chains.

## Deterministic in-toto provenance

Packaging emits an in-toto Statement v1 with a SLSA provenance v1 predicate.
Its subjects are the source ZIP, both SBOMs, and build information. Resolved
dependencies bind the upstream proof commit, Mathlib commit, elan installer Git
blob, Python lock digest, and GitHub Actions manifest digest. The statement is
itself checksummed, indexed, rebuilt twice, and independently verified before
release publication.

This deterministic statement describes the reproducible source recipe; it sets
`executionBound: false` and requires a hosted attestation. It therefore does not
claim that the release workflow ran. The separate GitHub attestations on tagged
artifacts provide that execution-bound evidence.
