# Supply-chain and release integrity

The artifact uses four independent integrity layers:

1. **Immutable mathematical dependency.** `lakefile.lean` and
   `archive/UPSTREAM.lock` pin the exact upstream proof commit; the upstream
   package pins Mathlib.
2. **Kernel verification.** CI compiles the publication wrappers and runs the
   axiom oracle on the three public endpoints.
3. **Source-tree manifest.** `MANIFEST.sha256` records every release source file
   other than itself.
4. **Archive sidecar.** Each deterministic release ZIP receives a separate
   SHA-256 file; `scripts/verify_release.py` checks the sidecar, ZIP integrity,
   archive-local manifest, required files, and forbidden legacy paths.

Tagged releases also request a GitHub artifact provenance attestation. The
attestation supplements, but does not replace, the source lock and Lean kernel
build.

Actions are updated through Dependabot. Before a high-assurance archival
release, the maintainer should review action updates, pin immutable action
revisions if required by the target institution, and retain the successful
workflow URL with the release metadata.
