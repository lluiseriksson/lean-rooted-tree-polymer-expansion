# Build status at package assembly

**Assembly date:** 2026-06-22

## Completed in this environment

- The supplied v1.0.0 archive was unpacked and structurally compared with the
  public repository README and theorem interface.
- The public Lean wrappers were checked against theorem names still present in
  upstream commit `4e45246aa109671d25fcd01ba1abf7bc3f8506d1`.
- The full article, bibliography, declarations, submission metadata, and figure
  source were migrated into the versioned documentation tree.
- Static claim, lock, metadata, placeholder, JSON/YAML, CFF-schema, and internal
  link audits passed.
- MkDocs built the complete site in strict mode.
- Python and shell scripts passed syntax checks.
- The deterministic source ZIP was generated twice with identical SHA-256
  output and passed archive-manifest verification.

## Deferred to GitHub Actions

Lean and outbound Git were unavailable in the package-assembly container, so a
fresh kernel rebuild could not be run here. The repository therefore includes:

- an exact Lean toolchain pin;
- an exact upstream commit pin;
- the upstream Mathlib pin;
- a clean-cache Lean CI job;
- an axiom-oracle invocation;
- strict documentation CI and Pages deployment;
- deterministic release checks and provenance attestation;
- explicit publication gates requiring a green CI URL before release.

A publishing agent must not describe the Lean build as freshly verified until
the uploaded repository's CI is green.
