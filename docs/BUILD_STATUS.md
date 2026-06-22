# Build status at artifact assembly

Date: 2026-06-22

## Completed in the assembly environment

- The LaTeX manuscript was compiled successfully to a 16-page PDF.
- The PDF was rendered page-by-page and visually inspected.
- Static artifact checks pass.
- The release archive and SHA-256 manifest are generated from a clean tree.
- The public Lean signatures were compared against the exact pinned upstream
  theorem statements and source blobs.

## Deferred to CI / publishing agent

The assembly container did not contain Lean or `elan`, and outbound Git access
was unavailable. Therefore the companion project was not kernel-rebuilt in this
container. The repository includes:

- an exact Lean toolchain pin;
- an exact upstream Git commit pin;
- the upstream Mathlib pin;
- a GitHub Actions Lean build;
- an axiom-oracle invocation;
- complete clean-build instructions.

Before submission, the publishing agent must run the clean CI build and record
its URL and final commit hash, as required by `docs/SUBMISSION_CHECKLIST.md`.
