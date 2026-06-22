# Marked Rooted-Tree Closure

**Machine-checked target-preserving leaf summation for polymer cluster expansions with holes.**

[Read the integrated paper](paper/index.md){ .md-button .md-button--primary }
[Reproduce the Lean build](artifact/reproducibility.md){ .md-button }

![Target-preserving proof pipeline](assets/images/proof-pipeline.png)

## Result at a glance

For complete-graph spanning trees on `n+1` labelled vertices, rooted at `0`,
with rooted child counts `c_T(v)`, the formalized combinatorial estimate is

$$
\frac{n+1}{(n+1)!}
\sum_T \prod_v c_T(v)! \le 4^n.
$$

Let `M` be the rooted/incompatible metric-moment constant and set
`L = 4 M^2`. The marked-root leaf sum then satisfies

$$
(n+1)S_n(r) \le M L^n,
$$

and, after extracting modified-metric target decay **before** forgetting the
exact union,

$$
T_n(Y) \le M e^{-\rho m(Y)} L^n.
$$

The three stable Lean endpoints are:

```lean
MarkedRootedClosure.normalizedRootedChildFactorialTreeBound
MarkedRootedClosure.markedRootLeafGeometricBound
MarkedRootedClosure.targetPreservingWeightedTreeBound
```

## Claims boundary

This repository proves finite combinatorics and its target-sensitive geometric
composition. It does **not** prove the model-specific raw Yang--Mills activity
bound, `hRpoly`, a continuum limit, Osterwalder--Schrader reconstruction, or a
continuum mass gap. See [Scope and limitations](paper/11-limitations.md).

## Publication model

The scholarly article is maintained directly as this versioned documentation
site. There is no separately tracked manuscript PDF: prose, formulas, theorem
maps, source provenance, and reproducibility instructions live in one reviewable
repository and are deployed together through GitHub Pages.
