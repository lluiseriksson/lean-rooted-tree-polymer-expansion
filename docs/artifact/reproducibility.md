# Reproducibility

## Standard verification

```bash
make docs-setup
make verify
```

This performs:

1. Lean compilation against the committed `lake-manifest.json`;
2. axiom-oracle execution and log audit;
3. generation of the continuous article from the canonical section manifest;
4. strict MkDocs build;
5. project-identity, dependency-lock, paper-manifest, metadata, link,
   placeholder, and source-tree audits.

The ordinary verification path does **not** run `lake update`.

## Explicit sequence

```bash
lake build MarkedRootedClosure
lake env lean MarkedRootedClosure/Oracle.lean | tee oracle.log
python3 scripts/check_oracle_output.py oracle.log
python3 scripts/assemble_paper.py
python3 -m mkdocs build --strict
make static
```

## Refreshing dependency locks

Only maintainers intending to update a dependency should run:

```bash
make lock-refresh
git diff -- lake-manifest.json lakefile.lean archive/UPSTREAM.lock
```

A lock change requires a dedicated review, a fresh oracle inspection, and a
clean-cache Lean CI run.

## Container verification

```bash
docker build -t lean-rooted-tree-polymer-expansion .
docker run --rm -v "$PWD:/workspace" -w /workspace \
  lean-rooted-tree-polymer-expansion make verify
```

The first build requires network access to retrieve the exact pinned Git
objects unless the Lake cache is already populated.

## Expected oracle boundary

The public endpoints should use only the standard classical principles inherited
from Lean/Mathlib, normally:

```text
propext
Classical.choice
Quot.sound
```

CI rejects `sorry`, `admit`, `sorryAx`, and project-local axiom declarations.

## Deterministic release

```bash
make package
```

The command produces:

- a source-only deterministic ZIP;
- a SHA-256 sidecar;
- an SPDX 2.3 JSON SBOM and its checksum.

CI creates the ZIP twice and requires byte-for-byte equality. The release
verifier checks the archive-local manifest, required files, forbidden legacy
paths, and all recorded hashes.

## Offline review boundary

The repository contains the article, theorem signatures, source locks, theorem
manifest, and exact theorem excerpts. A fresh Lean build still requires the
pinned dependencies or a populated cache. This is an explicit network
requirement, not an offline-build claim.
