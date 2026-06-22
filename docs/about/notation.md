# Notation and terminology

This page gives a quick reading key. Exact Lean types and hypotheses are listed
in the [formalization map](../formalization/index.md).

| Symbol | Meaning |
|---|---|
| $Q$ | A source-facing polymer in the finite system with holes |
| $Y$ | The exact target union of a polymer tuple |
| $\operatorname{skel}_{\mathcal H}(Q)$ | Active skeleton after removing or modifying hole regions |
| $d_M$ | Modified discrete metric used by the Appendix-F geometry |
| $m(Q)=d_M(Q)+1$ | Shifted metric length, always positive |
| $\mathsf E_\rho(Q)=e^{-\rho m(Q)}$ | Exponential metric weight |
| $T$ | A labelled tree on `n+1` vertices, rooted at `0` |
| $c_T(v)$ | Number of children of vertex $v$ in the rooted tree |
| $M$ | Finite hard-core metric-moment constant |
| $L=4M^2$ | Closed per-leaf ratio after tree-shape summation |
| $S_n(r)$ | Marked-root tree sum at order $n$ |
| $T_n(Y)$ | Exact-target weighted-tree term at order $n$ |

## “Marked root”

A root cube $r$ is selected in the active skeleton of the target. Marking the
root introduces the factor `n+1` that cancels the corresponding part of the
second-Ursell factorial normalization.

## “Closure”

Closure refers to replacing the remaining tree-shape and child-choice entropy
by an explicit geometric ratio. It does not mean topological closure and does
not denote a new cardinal notion of infinity.

## “With holes”

The geometry distinguishes the full target union from an active skeleton
modified by a finite family of separated holes. This distinction is central to
the target-sensitive composition theorem.
