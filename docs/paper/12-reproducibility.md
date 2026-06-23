# Reproducibility

The formal artifact and the article are versioned together. A clean verification
requires Git, a POSIX shell, Python 3, and `elan`.

From the repository root, run:

```bash
make docs-setup
make verify
```

This performs four independent classes of checks:

1. `make test` and `make syntax` exercise the repository tooling and validate
   Python and shell syntax;
2. `make lean` fetches the exact pinned upstream proof repository, compiles the
   publication companion, and audits the axiom oracle;
3. `make docs` builds this documentation site with MkDocs in strict mode;
4. `make static` validates identity, versions, Lean and Python locks, the proof
   DAG, theorem fingerprints, metadata, references, accessibility, internal
   links, workflows, and the absence of placeholder proofs or legacy
   standalone-paper artifacts.

The exact proof environment is recorded in `lean-toolchain`, `lakefile.lean`,
`lake-manifest.json`, and `archive/UPSTREAM.lock`. The exact documentation
Python environment is `requirements-docs.lock`. The publication endpoints and
their source chain are recorded in `archive/theorem-manifest.json` and
`archive/proof-dag.json`.

A deterministic source package can be created without rerunning Lean by using:

```bash
make package-determinism
```

A publication release should use `make release`, which first reruns the Lean
verification and then packages the tree. The release evidence includes the versioned ZIP and SHA-256 sidecar, SPDX and
CycloneDX SBOMs, build information, deterministic in-toto/SLSA provenance, a
release index, and aggregate checksums. The archive contains the integrated
article source under `docs/`; no separately tracked manuscript binary is
required. For long-term archival, tag an immutable commit, require green CI,
attach the complete generated evidence set, and record the resulting DOI only
after deposition.
