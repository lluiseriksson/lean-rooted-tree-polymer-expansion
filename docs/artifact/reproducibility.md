# Reproducibility

## Standard verification

```bash
make docs-setup
make verify
```

This performs:

1. focused repository-tooling tests plus Python and shell syntax checks;
2. Lean compilation against the committed `lake-manifest.json`;
3. exact axiom-oracle execution and log audit;
4. generation of the continuous article from the canonical section manifest;
5. strict MkDocs build;
6. project-identity, source-blob, statement-fingerprint, dependency-lock,
   Python-lock, proof-DAG, paper-manifest, reference, metadata,
   accessibility, link, workflow, agent-index, placeholder, and source-tree
   audits.

The ordinary verification path does **not** run `lake update`.

## Explicit sequence

```bash
lake build MarkedRootedClosure
lake env lean MarkedRootedClosure/Oracle.lean | tee oracle.log
python3 scripts/check_oracle_output.py oracle.log
make test
make syntax
python3 scripts/assemble_paper.py
python3 -m mkdocs build --strict
make static
```

## Python documentation environment

`requirements-docs.txt` records the four direct dependencies. The executable
reproducible environment is the exact transitive `requirements-docs.lock`, used
by local setup, CI, Pages, Docker, and the dev container. The lock audit rejects
range constraints, canonical-name duplicates, missing direct packages, and the
superseded CFF/minifier dependency chain.

## Refreshing dependency locks

Only maintainers intending to update a Lean dependency should run:

```bash
make lock-refresh
git diff -- lake-manifest.json lakefile.lean archive/UPSTREAM.lock
```

A lock change requires a dedicated review, refreshed source Git blob IDs and
statement excerpts where applicable, a fresh oracle inspection, and a
cold-cache Lean CI run.

## Container verification

```bash
docker build -t lean-rooted-tree-polymer-expansion .
docker run --rm -v "$PWD:/workspace" -w /workspace \
  lean-rooted-tree-polymer-expansion make verify
```

The Dockerfile pins the elan installer script by commit and verifies its Git
blob ID. The Lean toolchain itself is pinned separately in `lean-toolchain`.
The first build requires network access to retrieve exact Git objects unless the
Lake cache is already populated.

## Expected oracle boundary

Each public endpoint must report exactly:

```text
propext
Classical.choice
Quot.sound
```

The audit rejects missing reports, additional axioms, `sorry`, `admit`,
`sorryAx`, and project-local axiom declarations.

## Deterministic release

```bash
make package-determinism
```

The command produces:

- a source-only deterministic ZIP and per-file SHA-256 sidecar;
- SPDX 2.3 and CycloneDX 1.5 JSON SBOMs with checksums;
- deterministic build information;
- deterministic in-toto Statement v1 / SLSA provenance;
- a release evidence index;
- one aggregate SHA-256 file for all primary evidence.

The evidence set is built twice and must match byte-for-byte. The verifier
checks archive path safety, duplicate/case/Unicode collisions, file types,
member and total sizes, the archive-local manifest, required files, proof pins,
SBOM metadata and Python lock coverage, provenance subjects and resolved
dependencies, release-index records, and every recorded digest.
`make smoke-release` then extracts the ZIP into a temporary clean-room tree and
reruns dependency-free audits and tests.

## Scheduled drift detection

The monthly `scheduled-maintenance` workflow disables the Lean GitHub cache,
rebuilds the proof wrapper, builds the documentation, recreates deterministic
release evidence, and smoke-tests the archive. This detects dependency-service
or runner-image drift without changing any source lock.

## Offline review boundary

The repository contains the article, public theorem statements, signature
fingerprints, source Git blob IDs, source locks, theorem excerpts, and release
tooling. A fresh Lean build still requires the pinned dependencies or a
populated cache. This is an explicit network requirement, not an offline-build
claim.
