# Parent-normalized moment kernels

The tree-profile theorem controls shape entropy. The analytic-geometric
input controls the polymer assigned to each vertex.

## Hard-core moment kernel

Fix $\kappa_0>0$. For polymers $Q,Q'$ and a moment index
$j\in\mathbb N$, define $$K_j(Q,Q')
  =\mathbf 1_{\{Q\not\sim Q'\}}
    m(Q')^j\mathsf E_{2\kappa_0}(Q').$$ The hole geometry supplies a
constant $M=M(d,\kappa_0)\ge1$ such that $$\sum_{Q'}K_j(Q,Q')
  \le j!\,M^{j+1}\,m(Q).$$ There is also a rooted version: for every
active cube $r$, $$\sum_{Q:\,r\in\operatorname{skel}(Q)}m(Q)^j\mathsf E_{2\kappa_0}(Q)
  \le j!\,M^{j+1}.$$ The exact Lean theorem derives these from finite
modified-metric summability under explicit hole-disjointness,
no-inter-hole-edge, nonempty-hole, and numerical entropy hypotheses.

## Why normalization by the parent metric is necessary

The right-hand side of the child-moment estimate depends on the
parent $Q$ through $m(Q)$. A uniform tree-walk lemma cannot consume it
directly. The formal proof divides each nonroot edge factor by the
parent metric: $$\widetilde K_j(Q,Q')
  =\frac{m(Q')^jK_0(Q,Q')}{m(Q)}.$$ Since $m(Q)>0$, the child-moment estimate implies
$$\sum_{Q'}\widetilde K_j(Q,Q')
  \le j!\,M^{j+1}.$$

This division is not cosmetic. It is the algebraic move that converts a
parent-dependent budget into a local constant while retaining the
incompatibility edge.

## Global cancellation of parent metrics

For a fixed rooted tree $T$ and assignment $X:v\mapsto Q_v$, let
$p_T(v)$ be the parent of nonroot $v$. Then $$\prod_{v\ne0}m(Q_{p_T(v)})
  =\prod_{a=0}^{n}m(Q_a)^{c_T(a)}.$$ The denominators introduced in the normalized kernel therefore cancel exactly against the metric moments assigned to the
vertices. In Lean, this is proved from the partition of nonroot vertices
into rooted child fibers, not by informal multiplicity reasoning.
