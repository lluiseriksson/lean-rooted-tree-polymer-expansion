# Reproducibility

The formal artifact and the article are versioned together. A clean verification
requires Git, a POSIX shell, Python 3, and `elan`.

From the repository root, run:

```bash
make docs-setup
make verify
```

This performs three independent checks:

1. `make lean` fetches the exact pinned upstream proof repository, compiles the
   publication companion, and runs the axiom oracle;
2. `make docs` builds this documentation site with MkDocs in strict mode;
3. `make static` validates metadata, locks, public theorem names, internal
   links, the graphical abstract, and the absence of placeholder proofs or
   legacy standalone-paper artifacts.

The exact environment is recorded in `lean-toolchain`, `lakefile.lean`, and
`archive/UPSTREAM.lock`. The three publication-facing endpoints are also listed
in the machine-readable `archive/theorem-manifest.json`.

A deterministic source package can be created without rerunning Lean by using:

```bash
make package
```

A publication release should use `make release`, which first reruns the Lean
verification and then packages the tree. Both commands write a versioned ZIP and a SHA-256 sidecar to `release/`. The
archive contains the integrated article source under `docs/`; no separately
tracked manuscript binary is required. For long-term archival, tag an immutable
commit, require green CI, attach the generated source archive and checksum, and
record the resulting DOI in the citation metadata only after deposition.
