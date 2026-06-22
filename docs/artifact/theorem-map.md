# Theorem map

| Paper item | Companion theorem | Upstream theorem | Upstream file |
|---|---|---|---|
| Normalized tree-profile bound | `MarkedRootedClosure.normalizedRootedChildFactorialTreeBound` | `YangMills.KP.rootedChildCount_factorialTreeSum_normalized_le_four_pow` | `YangMills/KP/RootedLeafSummation.lean` |
| Marked-root leaf closure | `MarkedRootedClosure.markedRootLeafGeometricBound` | `YangMills.RG.appendixFHoleHsharpWeightedTreeMarkedRootSum_le_geometric_of_expWeight` | `YangMills/RG/AppendixFSecondUrsellLeafSummation.lean` |
| Target-preserving orderwise bound | `MarkedRootedClosure.targetPreservingWeightedTreeBound` | `YangMills.RG.appendixFHoleHsharpWeightedTreeTerm_le_geometric_of_expWeight_leafSummation` | `YangMills/RG/AppendixFSecondUrsellLeafSummation.lean` |

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
