# Public theorem signatures

The following are the full public theorem names exposed by the
companion:

    MarkedRootedClosure.normalizedRootedChildFactorialTreeBound
    MarkedRootedClosure.markedRootLeafGeometricBound
    MarkedRootedClosure.targetPreservingWeightedTreeBound

Their bodies are exact applications of the pinned upstream endpoints:

    YangMills.KP.rootedChildCount_factorialTreeSum_normalized_le_four_pow
    YangMills.RG.appendixFHoleHsharpWeightedTreeMarkedRootSum_le_geometric_of_expWeight
    YangMills.RG.appendixFHoleHsharpWeightedTreeTerm_le_geometric_of_expWeight_leafSummation

The full Lean signatures, including all geometry hypotheses, are
contained in the companion source file `PaperTheorems.lean`.
