# Lean Rooted-Tree Polymer Expansion

**Machine-checked target-preserving Ursell leaf summation for polymer systems with holes.**

> **Archived final state.** This repository is closed as a reproducible Lean 4
> proof artifact. The terminal published release is `v2.4.3`. It should not be
> read as an active claim of independent new mathematical theory; its value is
> the scoped machine-checked assembly, provenance, and verification record.
> See [`ARCHIVAL_NOTICE.md`](ARCHIVAL_NOTICE.md).

[![Lean verification](https://github.com/lluiseriksson/lean-rooted-tree-polymer-expansion/actions/workflows/ci.yml/badge.svg)](https://github.com/lluiseriksson/lean-rooted-tree-polymer-expansion/actions/workflows/ci.yml)
[![Documentation](https://github.com/lluiseriksson/lean-rooted-tree-polymer-expansion/actions/workflows/pages.yml/badge.svg)](https://lluiseriksson.github.io/lean-rooted-tree-polymer-expansion/)
[![Release](https://img.shields.io/github/v/release/lluiseriksson/lean-rooted-tree-polymer-expansion)](https://github.com/lluiseriksson/lean-rooted-tree-polymer-expansion/releases)
[![Lean](https://img.shields.io/badge/Lean-4.29.0--rc6-blue)](lean-toolchain)
[![Reproducible source](https://img.shields.io/badge/source-pinned-success)](archive/UPSTREAM.lock)
[![Code: AGPL v3+](https://img.shields.io/badge/code-AGPL--3.0--or--later-blue)](LICENSE)
[![Docs: CC BY 4.0](https://img.shields.io/badge/docs-CC%20BY%204.0-lightgrey)](docs/LICENSE.md)

This repository is a single-source publication artifact containing the complete
scholarly article, its Lean 4 companion, theorem provenance, reproducibility
instructions, CI, GitHub Pages deployment, and deterministic release tooling.
There is no separately maintained manuscript PDF.

**Current artifact release:** `v2.4.3`.

[**Read the integrated article**](https://lluiseriksson.github.io/lean-rooted-tree-polymer-expansion/paper/)
· [**Open the formalization map**](https://lluiseriksson.github.io/lean-rooted-tree-polymer-expansion/formalization/)
· [**Inspect the verification contract**](https://lluiseriksson.github.io/lean-rooted-tree-polymer-expansion/artifact/verification-contract/)

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

The theorem statements, normalized statement fingerprints, source paths, exact
upstream names, source Git blob IDs, and article sections are recorded in
[`archive/theorem-manifest.json`](archive/theorem-manifest.json) and
cross-checked against code and prose by
[`scripts/check_theorem_manifest.py`](scripts/check_theorem_manifest.py). The
machine-readable dependency chain between pinned upstream proofs and public
wrappers is recorded in [`archive/proof-dag.json`](archive/proof-dag.json).

## What is not proved

The artifact proves finite rooted-tree combinatorics and target-sensitive
geometric composition. It does **not** prove the model-specific raw
Yang--Mills activity estimate, `hRpoly`, a continuum construction,
Osterwalder--Schrader reconstruction, or a continuum mass gap. The full claims
boundary is maintained in [`docs/artifact/scope.md`](docs/artifact/scope.md).
No claim of independent novelty is made for the classical tree-graph or
combinatorial ingredients beyond their audited Lean assembly in this fixed
artifact.

## Verification

Requirements: Git, a POSIX shell, Python 3.11 or newer, and `elan`/Lean for an
optional local kernel run. The committed `lake-manifest.json` is authoritative;
ordinary verification does not run `lake update`.

For local source-package review, install the exact documentation environment and
run the complete non-Lean preflight:

```bash
make docs-setup
make verify-nonlean
make package-determinism
```

The authoritative Lean kernel build runs in GitHub Actions on the pinned Linux
environment. The Lean action performs one explicit `MarkedRootedClosure` build,
runs the pinned Lean environment checker, then `make lean-oracle` checks the
exact axiom set. A maintainer who deliberately wants the full local gate can run
`make lean` or `make verify`; these targets use a process-tree supervisor that
terminates all Lean/Lake descendants on timeout, interrupt, or parent-process
loss.

Useful targets:

```bash
make test              # focused unit tests for repository tooling
make syntax            # Python byte-compile and shell syntax validation
make verify-nonlean    # tests, strict docs, metadata, links, and static audits
make preflight         # alias of verify-nonlean
make lean-build        # supervised local wrapper compilation
make lean-oracle       # supervised exact-axiom oracle audit
make lean              # local build plus oracle; CI remains authoritative
make docs              # strict MkDocs build and generated one-page article
make static            # identity, locks, source manifest, metadata, workflows
make manifest          # explicitly refresh and review MANIFEST.sha256
make package           # ZIP, SBOMs, build info, provenance, release index
make package-determinism # build the complete evidence set twice byte-for-byte
make smoke-release     # safely extract the ZIP and audit it in a temporary tree
make release           # full local Lean verification plus deterministic package
make lock-refresh      # supervised dependency-lock refresh; review the full diff
```

The supervisor defaults are one hour for the build, ten minutes for the oracle,
and thirty minutes for an explicit lock refresh. They can be adjusted with
`LEAN_BUILD_TIMEOUT`, `LEAN_ORACLE_TIMEOUT`, and `LAKE_UPDATE_TIMEOUT` without
bypassing descendant cleanup. The exact pass criteria are documented in the
[verification contract](docs/artifact/verification-contract.md). Automated
agents can begin with [`docs/llms.txt`](docs/llms.txt).

## Release evidence

A tagged release contains exactly 13 files: six primary checksum subjects,
six canonical SHA-256 sidecars, and one ordered aggregate checksum file. The
set includes the deterministic source archive, SPDX 2.3 and CycloneDX 1.5
SBOMs, deterministic build information, a machine-readable release index, and
a non-execution-bound in-toto/SLSA declaration. A read-only job builds and
verifies that set; a separate tag-only job with publication permissions does
not check out or execute repository code, rejects any filename or checksum
drift, and attaches hosted GitHub provenance attestations before upload.
Together the records bind the archive, SBOMs, proof environment, complete
Python dependency lock, proof DAG, source manifests, declared release recipe,
and execution evidence by size and digest.

See [`docs/artifact/release-evidence.md`](docs/artifact/release-evidence.md).

## Immutable proof state

| Component | Pinned state |
|---|---|
| Upstream proofs | `lluiseriksson/THE-ERIKSSON-PROGRAMME@4e45246aa109671d25fcd01ba1abf7bc3f8506d1` |
| Lean | `leanprover/lean4:v4.29.0-rc6` |
| Mathlib | `07642720480157414db592fa85b626dafb71355b` |

The human-readable lock is [`archive/UPSTREAM.lock`](archive/UPSTREAM.lock),
the executable Lean dependency graph is committed in
[`lake-manifest.json`](lake-manifest.json), and the exact documentation tooling
environment is committed in [`requirements-docs.lock`](requirements-docs.lock).

## Stable identity

The public repository is
`lluiseriksson/lean-rooted-tree-polymer-expansion`; the stable Lean package and
namespace remain `MarkedRootedClosure`. The rename history and future migration
rules are recorded in [`REPOSITORY_HISTORY.md`](REPOSITORY_HISTORY.md).

## Publication model

The article begins at [`docs/paper/index.md`](docs/paper/index.md). During the
site build, [`scripts/assemble_paper.py`](scripts/assemble_paper.py) creates a
single continuous HTML article from the same canonical section sources. Readers
can therefore use sectional navigation or one-page reading without introducing
a second manuscript source.

The standalone v2.4.2 PDF/LaTeX bundle is a historical typeset export. It does
not replace the integrated article, theorem manifest, CI logs, or deterministic
release evidence in `v2.4.3`.

## Citation and licensing

Use [`CITATION.cff`](CITATION.cff) or [`CITATION.bib`](CITATION.bib). Add an
archive DOI only after the exact verified release has been deposited.

Lean code and repository tooling are AGPL-3.0-or-later. Original scholarly
documentation and figures are CC BY 4.0; see [`docs/LICENSE.md`](docs/LICENSE.md).
