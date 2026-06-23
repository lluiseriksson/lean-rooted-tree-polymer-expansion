# Lean formalization map

The companion package keeps the public API small. Each theorem below is a
transparent alias of a proved theorem in the pinned upstream repository.

| Public theorem | Mathematical role | Upstream theorem | Article section |
|---|---|---|---|
| `MarkedRootedClosure.normalizedRootedChildFactorialTreeBound` | Closes complete-tree shape entropy by $4^n$ after the Ursell normalization | `YangMills.KP.rootedChildCount_factorialTreeSum_normalized_le_four_pow` | [Rooted tree profile](../paper/03-rooted-tree-profile.md) |
| `MarkedRootedClosure.markedRootLeafGeometricBound` | Bounds the marked-root second-Ursell leaf sum by $M(4M^2)^n$ | `YangMills.RG.appendixFHoleHsharpWeightedTreeMarkedRootSum_le_geometric_of_expWeight` | [Marked-root closure](../paper/06-marked-root-closure.md) |
| `MarkedRootedClosure.targetPreservingWeightedTreeBound` | Extracts exact-target modified-metric decay before applying the rooted overcount | `YangMills.RG.appendixFHoleHsharpWeightedTreeTerm_le_geometric_of_expWeight_leafSummation` | [Target-preserving decay](../paper/07-target-preserving-decay.md) |

## Stable package interface

```lean
import MarkedRootedClosure
```

The theorem declarations live in
[`MarkedRootedClosure/PaperTheorems.lean`](https://github.com/lluiseriksson/lean-rooted-tree-polymer-expansion/blob/main/MarkedRootedClosure/PaperTheorems.lean).
The machine-readable correspondence is
[`archive/theorem-manifest.json`](https://github.com/lluiseriksson/lean-rooted-tree-polymer-expansion/blob/main/archive/theorem-manifest.json).

## Proof trust

The oracle command

```bash
lake env lean MarkedRootedClosure/Oracle.lean
```

prints the axioms used by the three public endpoints. CI rejects `sorry`,
`admit`, `sorryAx`, and project-local axiom declarations. The intended output
contains only the standard classical axioms inherited from Lean/Mathlib:

```text
propext
Classical.choice
Quot.sound
```

## Dependency pin

The package depends on one exact upstream commit and commits the resulting
`lake-manifest.json`. Ordinary builds consume that manifest; refreshing it is a
separate, explicit maintenance operation.

| Component | Revision |
|---|---|
| `THE-ERIKSSON-PROGRAMME` | `4e45246aa109671d25fcd01ba1abf7bc3f8506d1` |
| Mathlib | `07642720480157414db592fa85b626dafb71355b` |
| Lean | `v4.29.0-rc6` |

## Repository identity and API stability

The public repository rename is complete. The GitHub slug and release archive
names use `lean-rooted-tree-polymer-expansion`, while the Lean package and
namespace remain `MarkedRootedClosure`. This separates public discoverability
from formal API stability and preserves downstream imports.

## Statement-fingerprint policy

The public declarations are fingerprinted after removing comments and
normalizing whitespace, while excluding proof terms. The resulting SHA-256
values are stored in `archive/theorem-manifest.json` and recomputed during the
static audit. This catches semantic changes to binders, assumptions, constants,
or conclusions even if theorem names and upstream references remain unchanged.

The manifest also records the exact Git blob IDs of the two upstream Lean source
files. The fingerprint and blob checks complement, but never replace, kernel
compilation.
