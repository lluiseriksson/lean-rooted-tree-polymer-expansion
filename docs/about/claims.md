# Claims and scope

The central publication claim is deliberately narrow.

The repository is now closed as an archival proof artifact. No active claim is
made that the manuscript contains independent mathematical novelty beyond the
scoped Lean formalization, proof decomposition, and reproducibility record.

## Kernel-checked claims

The Lean companion exposes three theorems:

1. a normalized aggregate bound on rooted child-factorial tree weights;
2. a marked-root geometric leaf-summation bound for the finite second Ursell
   expansion with holes; and
3. an orderwise target-preserving weighted-tree bound obtained by extracting
   the exact target decay before applying the marked-root estimate.

Their complete signatures are available in the
[formalization map](../formalization/index.md) and
[`MarkedRootedClosure/PaperTheorems.lean`](https://github.com/lluiseriksson/lean-rooted-tree-polymer-expansion/blob/main/MarkedRootedClosure/PaperTheorems.lean).

## Mathematical corollary stated in the article

When an activity contributes an additional factor $\varepsilon^{n+1}$, the
orderwise estimate yields the ordinary geometric majorant

$$
\sum_{n\ge0}
M\varepsilon e^{-\rho m(Y)}(4M^2\varepsilon)^n
=
\frac{M\varepsilon}{1-4M^2\varepsilon}
 e^{-\rho m(Y)},
$$

provided $4M^2\varepsilon<1$. The repository distinguishes this elementary
series consequence from the finite orderwise Lean endpoints.

## Explicitly excluded claims

The artifact does not establish any of the following:

- a concrete raw Yang--Mills activity estimate from the physical fluctuation
  integral;
- the project hypothesis commonly denoted `hRpoly`;
- an ultraviolet or infinite-volume continuum construction;
- Osterwalder--Schrader or Wightman reconstruction;
- a continuum Yang--Mills mass gap;
- a theorem about cardinal infinities or the hypothesis of Riemann.

These statements may motivate the surrounding research programme, but none is
silently imported into this artifact.

## Why this boundary matters

Formal verification can certify only the theorem actually stated. A clean
claims boundary prevents an abstract interface, a finite-volume estimate, or a
conditional consumer theorem from being presented as a physical construction.
The boundary is repeated in the README, article, theorem manifest, evaluator
guide, and release metadata so it survives citation outside the repository.
The same boundary also prevents the artifact from being read as a broader
publication claim after archival.
