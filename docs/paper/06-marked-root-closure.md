# Marked-root geometric closure

## The marked-root sum

Let $\mathsf S_n(r)$ be the normalized nonnegative tree sum in which
coordinate $0$ is constrained by $r\in\operatorname{skel}(Q_0)$. Marking
one coordinate of an $(n+1)$-tuple creates an outer factor $n+1$. The
Ursell normalization contributes $(n+1)!^{-1}$. This is precisely the normalization in the [rooted tree-profile theorem](03-rooted-tree-profile.md).

<div id="thm:marked-root" class="theorem" markdown="1">

**Theorem 4** (Marked-root leaf summation). *Under the explicit
hole-geometry and metric-summability hypotheses of the Lean statement,
$$(n+1)\mathsf S_n(r)
  \le M\,(4M^2)^n.$$*

</div>

<div class="proof" markdown="1">

*Assembly.* The raw incompatibility-tree sum is first bounded by a sum
over complete-graph tree shapes that retains a hard-core indicator on
each BFS parent edge. The vertex weights are then dominated by the spare
exponential weight entering the moment kernel. Applying the [fixed-tree estimate](05-fixed-tree-elimination.md#fixed-tree-bound) and summing shapes gives
$$(n+1)\mathsf S_n(r)
  \le
  \frac{n+1}{(n+1)!}
  M^{2n+1}
  \sum_T\prod_vc_T(v)!.$$
The [rooted tree-profile theorem](03-rooted-tree-profile.md) yields $$(n+1)\mathsf S_n(r)
  \le M^{2n+1}4^n
  =M(4M^2)^n.$$ The Lean theorem names the closed leaf ratio
$$L(d,\kappa_0)=4M(d,\kappa_0)^2.$$ ◻

</div>

![Target-preserving proof pipeline](../assets/images/proof-pipeline.png)

*The proof order: the exact target is used before the marked-root
enlargement, and tree edges are retained until child variables have been
locally summed.*
