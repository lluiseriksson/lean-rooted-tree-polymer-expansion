# Theorem map

| Paper item | Companion theorem | Upstream theorem | Upstream file | Source Git blob |
|---|---|---|---|---|
| Normalized tree-profile bound | `MarkedRootedClosure.normalizedRootedChildFactorialTreeBound` | `YangMills.KP.rootedChildCount_factorialTreeSum_normalized_le_four_pow` | `YangMills/KP/RootedLeafSummation.lean` | `1415686403c26536da8736a9021237773c7467dc` |
| Marked-root leaf closure | `MarkedRootedClosure.markedRootLeafGeometricBound` | `YangMills.RG.appendixFHoleHsharpWeightedTreeMarkedRootSum_le_geometric_of_expWeight` | `YangMills/RG/AppendixFSecondUrsellLeafSummation.lean` | `0307d11b95d4385d4ea39067290e7eec929cd7f6` |
| Target-preserving orderwise bound | `MarkedRootedClosure.targetPreservingWeightedTreeBound` | `YangMills.RG.appendixFHoleHsharpWeightedTreeTerm_le_geometric_of_expWeight_leafSummation` | `YangMills/RG/AppendixFSecondUrsellLeafSummation.lean` | `0307d11b95d4385d4ea39067290e7eec929cd7f6` |

The exact typed statements and signature fingerprints are recorded in
[`archive/theorem-manifest.json`](https://github.com/lluiseriksson/lean-rooted-tree-polymer-expansion/blob/main/archive/theorem-manifest.json).

## Dependency ladder

```text
parent-map fiber profiles
  -> fixed-profile factorial budget
  -> central-binomial profile count
  -> normalized 4^n tree bound
  -> parent-normalized incompatibility kernel
  -> fixed-tree bottom-up walk bound
  -> root metric moment
  -> marked-root orderwise leaf bound
  -> fixed-union metric stitching
  -> target-preserving weighted-tree bound
```

## Why the target must be retained

The exact union `Y` and the incompatibility tree are retained while

```text
m(Y) <= sum_i m(Q_i)
```

is applied. Only after `exp(-rate * m(Y))` has been extracted is the exact-union
fiber enlarged to a marked-root overcount. Reversing the order loses the target
and cannot produce target decay without reintroducing it as an assumption.
