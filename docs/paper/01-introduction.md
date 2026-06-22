# Introduction

Cluster expansions convert logarithms of partition functions into sums
over connected configurations. Their conceptual statement is simple, but
quantitative constructive applications require unusually strict
information discipline. In a polymer expansion with holes, two pieces of
information are especially easy to lose:

1.  the *exact target union* $Y$, which carries the geometric decay
    needed by the downstream renormalization-group estimate;

2.  the *local tree structure*, which is needed to sum one child polymer
    through its incompatibility relation with its parent.

If either is discarded prematurely, a finite sum remains, but the
desired volume-uniform, target-dependent bound need not.

This paper isolates and formalizes a proof order that preserves both.
The exact target fiber is retained while a stitching inequality extracts
a factor $e^{-\rho m(Y)}$. Only then is a root cube
$r\in\operatorname{skel}(Y)$ marked and the target fiber enlarged to a
rooted overcount. At fixed tree shape, nonroot variables are eliminated
from the leaves inward. A normalization by the parent metric cancels
globally because every appearance of a vertex as a parent is counted by
its rooted child count. The remaining factorial degree weights are
summed over labelled trees using a parent-profile argument.

The resulting formalized mechanism is summarized by
$$\boxed{\begin{gathered}
\text{exact target fiber}\to\text{target decay}\to\text{marked root}\\
\to\text{local leaf recursion}\to 4^n\text{ closure}
\end{gathered}}$$

The construction belongs to the classical lineage of tree-graph
identities and abstract polymer expansions (Penrose 1967; Kotecký and
Preiss 1986; Fernández and Procacci 2007; Brydges 1986). Its
source-facing motivation is the with-holes renormalization-group
organization in the Balaban--Dimock literature (Dimock 2013a, 2013b,
2014). The contribution here is an end-to-end Lean 4 decomposition of a
specific target-preserving leaf-summation mechanism, with explicit
constants and a reproducible theorem map. Lean 4 and Mathlib provide the
proof environment (Moura and Ullrich 2021; The mathlib Community 2020);
the work also fits a broader recent effort to formalize mathematically
structured quantum field theory (Douglas et al. 2026).

## Why this is an “infinity” result only in a controlled sense

The motivating language of “marked infinities” is not cardinal
arithmetic. It refers to a recurring analytic principle: when an
infinite or eventually infinite expansion is approached through finite
truncations, the physically relevant information is often a marker—a
root, target, boundary condition, or direction of approach—that must
survive until a uniform estimate has been extracted. The present theorem
is entirely finite at each order $n$. Its purpose is to produce a
geometric ratio that can later justify an infinite order sum.

## Contributions

The formalized result has four publication-facing layers.

1.  A normalized aggregate bound for rooted child-factorial weights of
    complete-graph spanning trees: $$\frac{n+1}{(n+1)!}
        \sum_{T\in\mathcal T_{n+1}}
        \prod_{v=0}^{n} c_T(v)!
        \le 4^n.$$

2.  A parent-normalized hard-core moment kernel whose local sums are
    factorially controlled.

3.  A marked-root fixed-tree recursion and its aggregate consequence
    $$(n+1)\mathsf S_n(r)\le M(4M^2)^n.$$

4.  A target-preserving composition theorem $$\mathsf T_n(Y)\le M\,\mathsf E_\rho(Y)(4M^2)^n,$$ where
    $\mathsf E_\rho(Y)=e^{-\rho m(Y)}$ in the source-facing
    specialization.

The companion project exposes these layers as three short theorem names
while retaining the full hypotheses of the verified upstream statements.

## Scope

The formalization does not construct a concrete Yang--Mills fluctuation
activity. In particular, it does not prove the analytic estimate that
would identify a physical activity with the abstract polymer weight
entering the theorem. It also does not prove a continuum limit,
Osterwalder--Schrader reconstruction, or a continuum mass gap. These
exclusions are mathematical boundaries, not editorial caveats.
