# Marked Rooted-Tree Summation for Polymer Expansions with Holes

[![Lean CI](https://github.com/lluiseriksson/marked-rooted-closure/actions/workflows/ci.yml/badge.svg)](https://github.com/lluiseriksson/marked-rooted-closure/actions/workflows/ci.yml)
[![Documentation](https://github.com/lluiseriksson/marked-rooted-closure/actions/workflows/pages.yml/badge.svg)](https://lluiseriksson.github.io/marked-rooted-closure/)
[![Lean](https://img.shields.io/badge/Lean-4.29.0--rc6-blue)](lean-toolchain)
[![Source pinned](https://img.shields.io/badge/upstream-pinned-success)](archive/UPSTREAM.lock)
[![License: AGPL v3+](https://img.shields.io/badge/code-AGPL--3.0--or--later-blue)](LICENSE)

This repository is a documentation-integrated publication artifact: the paper,
Lean 4 companion, theorem map, source provenance, CI, evaluation guide, and
release tooling are maintained in one versioned tree.

[**Read the integrated paper**](https://lluiseriksson.github.io/marked-rooted-closure/paper/)

![Proof pipeline](docs/assets/images/proof-pipeline.png)

## Mathematical result

The artifact formalizes a finite, target-preserving rooted-tree leaf-summation
mechanism for a second Ursell expansion with holes. It keeps the exact target
union until modified-metric decay has been extracted, marks a root in the
active skeleton, performs a parent-normalized bottom-up moment recursion, and
closes tree-shape entropy by a normalized `4^n` bound.

The stable publication-facing Lean endpoints are:

```lean
MarkedRootedClosure.normalizedRootedChildFactorialTreeBound
MarkedRootedClosure.markedRootLeafGeometricBound
MarkedRootedClosure.targetPreservingWeightedTreeBound
```

For rooted child counts `c_T(v)`, the core formulas are

$$
\frac{n+1}{(n+1)!}\sum_T\prod_v c_T(v)!\le 4^n,
$$

$$
(n+1)S_n(r)\le M(4M^2)^n,
$$

and

$$
T_n(Y)\le M e^{-\rho m(Y)}(4M^2)^n.
$$

## Paper-as-documentation

There is no separately tracked manuscript PDF. The article begins at
[`docs/paper/index.md`](docs/paper/index.md) and is rendered as the GitHub Pages
site configured by [`mkdocs.yml`](mkdocs.yml). This prevents drift between the
paper, theorem map, and artifact documentation.

## Verify

Requirements: Git, a POSIX shell, Python 3 with `venv`, and `elan`/Lean.
`make docs-setup` creates an isolated documentation environment. The first Lean
build fetches the exact pinned upstream project and Mathlib revision.

```bash
make docs-setup
make verify
```

Individual targets:

```bash
make lean       # compile wrappers and run axiom oracle
make docs       # strict MkDocs build
make static     # metadata, links, locks, placeholders
make package    # docs/static checks + deterministic ZIP
make release    # Lean verification + package
```

See [reproducibility](docs/artifact/reproducibility.md) and the
[artifact evaluation guide](docs/artifact/evaluation.md).

## Immutable proof source

- Upstream: `lluiseriksson/THE-ERIKSSON-PROGRAMME`
- Commit: `4e45246aa109671d25fcd01ba1abf7bc3f8506d1`
- Lean: `leanprover/lean4:v4.29.0-rc6`
- Mathlib: `07642720480157414db592fa85b626dafb71355b`

The machine-readable lock is [`archive/UPSTREAM.lock`](archive/UPSTREAM.lock).

## Scope

This artifact proves finite combinatorics and target-sensitive geometric
composition. It does **not** prove the model-specific raw Yang--Mills activity
bound, `hRpoly`, a continuum limit, Osterwalder--Schrader reconstruction, or a
continuum mass gap. See [Novelty and scope](docs/artifact/scope.md).

## Uploading this v2 tree

The existing GitHub repository contains the previous PDF-based bundle. Upload
this version with a delete-aware copy so legacy `paper/` and
`release-artifacts/` directories are removed. See
[upload and migration instructions](docs/maintainers/upload-and-migration.md).

## Citation

Use [`CITATION.cff`](CITATION.cff) or [`CITATION.bib`](CITATION.bib). Add an
archive DOI only after the verified release has been deposited.

## License

Lean code and repository tooling are distributed under
AGPL-3.0-or-later. The integrated scholarly documentation remains copyright
Lluis Eriksson; see [`docs/LICENSE.md`](docs/LICENSE.md).
