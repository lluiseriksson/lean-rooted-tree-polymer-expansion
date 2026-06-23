# Reproducibility

The formal artifact and the article are versioned together. Local source-package
review requires Git, a POSIX shell, and Python 3.11 or newer.

From the repository root, run:

```bash
make docs-setup
make verify-nonlean
make package-determinism
```

This performs four independent classes of non-Lean checks:

1. `make test` and `make syntax` exercise the repository tooling and validate
   Python and shell syntax;
2. `make docs` builds this documentation site with MkDocs in strict mode;
3. `make static` validates identity, versions, Lean and Python locks, the proof
   DAG, theorem fingerprints, metadata, references, accessibility, internal
   links, workflows, and the absence of placeholder proofs or legacy
   standalone-paper artifacts;
4. deterministic packaging builds the complete evidence set twice and audits a
   safely extracted clean-room copy.

The authoritative kernel gate runs in GitHub Actions. The pinned Lean action
builds `MarkedRootedClosure` once in the expected Linux environment, runs the
pinned environment checker, and the next step runs `make lean-oracle` to require
the exact documented axiom set. A maintainer may reproduce the build and oracle
phases locally with:

```bash
make lean
```

The local target supervises the whole Lean/Lake process group. Timeout,
interrupt, or loss of the invoking parent terminates all descendants and cannot
silently leave workers running. It also requires `lake-manifest.json` to remain
byte-identical.

The exact proof environment is recorded in `lean-toolchain`, `lakefile.lean`,
`lake-manifest.json`, and `archive/UPSTREAM.lock`. The exact documentation
Python environment is `requirements-docs.lock`. The publication endpoints and
their source chain are recorded in `archive/theorem-manifest.json` and
`archive/proof-dag.json`.

The release evidence includes the versioned ZIP and SHA-256 sidecar, SPDX and
CycloneDX SBOMs, build information, a deterministic in-toto/SLSA declaration, a
release index, and aggregate checksums. The deterministic declaration binds the
recipe and dependencies but explicitly does not claim hosted execution. Tagged
releases add separate GitHub provenance attestations. The archive contains the
integrated article source under `docs/`; no separately tracked manuscript binary
is required.
