# Supply-chain and release integrity

The artifact uses complementary integrity layers.

1. **Immutable proof dependency.** `lakefile.lean`, `lake-manifest.json`, and
   `archive/UPSTREAM.lock` agree on the exact upstream and Mathlib revisions.
2. **Kernel verification.** CI compiles the public wrappers and runs the axiom
   oracle.
3. **Claims manifest.** `archive/theorem-manifest.json` maps every public theorem
   to its upstream name, source file, and article section.
4. **Source-tree manifest.** `MANIFEST.sha256` records each packaged source file
   other than itself.
5. **Deterministic archive.** ZIP timestamps, permissions, ordering, and root
   directory are normalized; CI requires two independent builds to match
   byte-for-byte.
6. **Archive sidecar.** A separate SHA-256 file authenticates the ZIP.
7. **Software bill of materials.** Packaging emits SPDX 2.3 JSON covering the
   root artifact, locked Lean packages, and pinned documentation dependencies.
8. **Hosted provenance.** Tagged releases request a GitHub build-provenance
   attestation.

The release verifier checks the ZIP sidecar, member integrity, archive-local
manifest, required files, forbidden paths, and absence of tracked PDF/ZIP
binaries inside the source archive.

GitHub Actions and Python documentation packages are monitored by Dependabot.
For institutions requiring immutable action revisions, a maintainer should pin
reviewed action commits in a dedicated security change and preserve the
successful workflow URL with the archival metadata.
