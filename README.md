# Marked Rooted-Tree Summation for Polymer Expansions with Holes

[![Lean](https://img.shields.io/badge/Lean-4.29.0--rc6-blue)](lean-toolchain)
[![Source](https://img.shields.io/badge/source-pinned-success)](archive/UPSTREAM.lock)
[![Paper](https://img.shields.io/badge/paper-PDF-b31b1b)](paper/main.pdf)
[![License: AGPL v3+](https://img.shields.io/badge/code-AGPL--3.0--or--later-blue)](LICENSE)

This repository is a publication bundle: manuscript, Lean 4 companion, exact
source locks, theorem map, CI, artifact checks, citation metadata, graphical
abstract, and submission handoff.

![Proof pipeline](paper/graphical-abstract.png)

The mathematical result is a **finite, target-preserving rooted-tree
leaf-summation theorem** for a second Ursell expansion with holes. It keeps the
exact target union until modified-metric decay has been extracted, marks a root
in the active skeleton, performs a parent-normalized bottom-up moment recursion,
and closes tree-shape entropy by a normalized `4^n` bound.

The three publication-facing Lean endpoints are:

```lean
MarkedRootedClosure.normalizedRootedChildFactorialTreeBound
MarkedRootedClosure.markedRootLeafGeometricBound
MarkedRootedClosure.targetPreservingWeightedTreeBound
```

They re-export machine-checked proofs from `THE-ERIKSSON-PROGRAMME` at the exact
commit recorded in [`archive/UPSTREAM.lock`](archive/UPSTREAM.lock). Lean,
Mathlib, upstream source files, and Git blobs are pinned.

## Main formulas

For complete-graph spanning trees on `n+1` labelled vertices, rooted at `0`,
with `c_T(v)` children at vertex `v`, the formalized bound is

\[
\frac{n+1}{(n+1)!}
\sum_T \prod_v c_T(v)! \le 4^n.
\]

Let `M` be the rooted/incompatible metric-moment constant and `L = 4 M^2`. The
marked-root leaf sum satisfies

\[
(n+1)S_n(r) \le M L^n.
\]

After extracting target decay before forgetting the exact union,

\[
T_n(Y) \le M\,e^{-\rho m(Y)}L^n.
\]

Consequently, whenever an activity contributes `epsilon^(n+1)` and
`L epsilon < 1`, the order sum is bounded by

\[
\frac{M\epsilon}{1-L\epsilon}\,e^{-\rho m(Y)}.
\]

The last formula is the geometric-series corollary of the finite orderwise Lean
endpoints.

## Build

Requirements: Git, a POSIX shell, and `elan`/Lean. No global Mathlib install is
required.

```bash
make lean
make paper
make audit
```

Or run everything:

```bash
make all
```

The first Lean build fetches the exact pinned upstream project and its pinned
Mathlib commit. See [`docs/BUILD_STATUS.md`](docs/BUILD_STATUS.md) for the
assembly-environment verification record.

## Paper and submission bundle

- [Manuscript PDF](paper/main.pdf)
- [LaTeX source](paper/main.tex)
- [Graphical abstract](paper/graphical-abstract-final.pdf)
- [Cover letter](paper/cover-letter.md)
- [ArXiv abstract](paper/arxiv-abstract.txt)
- [Submission metadata](paper/submission-metadata.yaml)
- [Original release artifacts](release-artifacts/README.md)

## Scope

This artifact proves finite combinatorics and its target-sensitive geometric
composition. It does **not** prove the model-specific raw Yang-Mills activity
bound, `hRpoly`, a continuum limit, Osterwalder-Schrader reconstruction, or a
continuum mass gap. See [`docs/NOVELTY_AND_SCOPE.md`](docs/NOVELTY_AND_SCOPE.md).

## Review map

- [Reproducibility](docs/REPRODUCIBILITY.md)
- [Source provenance](docs/SOURCE_PROVENANCE.md)
- [Theorem map](docs/THEOREM_MAP.md)
- [Artifact evaluation](docs/ARTIFACT_EVALUATION.md)
- [Publishing-agent handoff](docs/AGENT_HANDOFF.md)
- [Submission checklist](docs/SUBMISSION_CHECKLIST.md)

## Release

```bash
make release
```

This rebuilds the paper, runs the static artifact audit, and produces a clean
versioned ZIP plus SHA-256 file in `release/`.

The externally supplied ZIP, SHA-256 sidecar, and PDF copy used to assemble this
repository are preserved under [`release-artifacts/`](release-artifacts/).

## License

The Lean companion is AGPL-3.0-or-later, matching the pinned upstream project.
The manuscript licensing decision is documented separately in
[`paper/LICENSE.md`](paper/LICENSE.md) for the publishing agent.
