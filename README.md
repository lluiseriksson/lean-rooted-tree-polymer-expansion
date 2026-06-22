# Lean Rooted-Tree Polymer Expansion

**Machine-checked target-preserving Ursell leaf summation for polymer systems with holes.**

[![Lean verification](https://github.com/lluiseriksson/lean-rooted-tree-polymer-expansion/actions/workflows/ci.yml/badge.svg)](https://github.com/lluiseriksson/lean-rooted-tree-polymer-expansion/actions/workflows/ci.yml)
[![Documentation](https://github.com/lluiseriksson/lean-rooted-tree-polymer-expansion/actions/workflows/pages.yml/badge.svg)](https://lluiseriksson.github.io/lean-rooted-tree-polymer-expansion/)
[![Lean](https://img.shields.io/badge/Lean-4.29.0--rc6-blue)](lean-toolchain)
[![Reproducible source](https://img.shields.io/badge/source-pinned-success)](archive/UPSTREAM.lock)
[![Code: AGPL v3+](https://img.shields.io/badge/code-AGPL--3.0--or--later-blue)](LICENSE)
[![Docs: CC BY 4.0](https://img.shields.io/badge/docs-CC%20BY%204.0-lightgrey)](docs/LICENSE.md)

This repository is a single-source publication artifact containing the complete
scholarly article, its Lean 4 companion, theorem provenance, reproducibility
instructions, CI, GitHub Pages deployment, and deterministic release tooling.
There is no separately maintained manuscript PDF.

**Current artifact release:** `v2.1.0`.

[**Read the integrated article**](https://lluiseriksson.github.io/lean-rooted-tree-polymer-expansion/paper/)
· [**Open the formalization map**](https://lluiseriksson.github.io/lean-rooted-tree-polymer-expansion/formalization/)
· [**Reproduce the artifact**](https://lluiseriksson.github.io/lean-rooted-tree-polymer-expansion/artifact/reproducibility/)

![Target-preserving rooted-tree proof pipeline](docs/assets/images/proof-pipeline.png)

## What is proved

For complete-graph spanning trees on `n+1` labelled vertices, rooted at `0`,
with rooted child counts `c_T(v)`, the machine-checked combinatorial estimate is

$$
\frac{n+1}{(n+1)!}\sum_T\prod_v c_T(v)!\le 4^n.
$$

Let `M` be the hard-core metric-moment constant and set `L = 4M^2`. The
formalization then proves the marked-root orderwise estimate

$$
(n+1)S_n(r)\le M L^n,
$$

and, after extracting the exact target-union decay before passing to the rooted
overcount,

$$
T_n(Y)\le M e^{-\rho m(Y)}L^n.
$$

The stable publication-facing Lean endpoints are:

```lean
MarkedRootedClosure.normalizedRootedChildFactorialTreeBound
MarkedRootedClosure.markedRootLeafGeometricBound
MarkedRootedClosure.targetPreservingWeightedTreeBound
```

The theorem statements, source paths, exact upstream names, and paper sections
are recorded in [`archive/theorem-manifest.json`](archive/theorem-manifest.json).

## What is not proved

The artifact proves finite rooted-tree combinatorics and target-sensitive
geometric composition. It does **not** prove the model-specific raw
Yang--Mills activity estimate, `hRpoly`, a continuum construction,
Osterwalder--Schrader reconstruction, or a continuum mass gap. The full claims
boundary is maintained in [`docs/artifact/scope.md`](docs/artifact/scope.md).

## Deterministic verification

Requirements: Git, a POSIX shell, Python 3.11 or newer, and `elan`/Lean. The
committed `lake-manifest.json` is authoritative; ordinary verification does not
run `lake update`.

```bash
make docs-setup
make verify
```

Useful targets:

```bash
make lean          # compile the wrappers and inspect theorem axioms
make docs          # strict MkDocs build, including the generated full article
make static        # identity, locks, metadata, links, paper manifest, placeholders
make package       # deterministic source ZIP, checksum, and SPDX SBOM
make release       # complete Lean verification plus packaging
make lock-refresh  # explicit dependency-lock refresh; review the resulting diff
```

A clean-room Docker command is documented in
[`docs/artifact/reproducibility.md`](docs/artifact/reproducibility.md).

## Immutable proof state

| Component | Pinned state |
|---|---|
| Upstream proofs | `lluiseriksson/THE-ERIKSSON-PROGRAMME@4e45246aa109671d25fcd01ba1abf7bc3f8506d1` |
| Lean | `leanprover/lean4:v4.29.0-rc6` |
| Mathlib | `07642720480157414db592fa85b626dafb71355b` |

The human-readable lock is [`archive/UPSTREAM.lock`](archive/UPSTREAM.lock),
and the executable dependency graph is committed in [`lake-manifest.json`](lake-manifest.json).

## Repository name

The current slug, `marked-rooted-closure`, is historically accurate but not
self-explanatory outside the project. The recommended public name is:

> **`lean-rooted-tree-polymer-expansion`**

which would produce the clearer URL
`https://lluiseriksson.github.io/lean-rooted-tree-polymer-expansion/`.
The proposal, impact analysis, exact GitHub steps, and an idempotent metadata
migration command are in [`REPOSITORY_RENAME.md`](REPOSITORY_RENAME.md). A repo
rename does not change the stable Lean namespace `MarkedRootedClosure`.

## Publication model

The article begins at [`docs/paper/index.md`](docs/paper/index.md). During the
site build, [`scripts/assemble_paper.py`](scripts/assemble_paper.py) also creates
a single continuous HTML article from the same section sources. Thus readers
can use either sectional navigation or one-page reading without introducing a
second manuscript source.

## Citation and licensing

Use [`CITATION.cff`](CITATION.cff) or [`CITATION.bib`](CITATION.bib). Add an
archive DOI only after a verified release has been deposited.

Lean code and repository tooling are AGPL-3.0-or-later. Original scholarly
documentation and figures are CC BY 4.0; see [`docs/LICENSE.md`](docs/LICENSE.md).
