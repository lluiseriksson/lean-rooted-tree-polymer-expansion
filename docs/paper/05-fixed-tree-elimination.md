# Fixed-tree leaf elimination

We now combine the normalized budgets along one tree.

## Vertexwise tree walk

A generic finite theorem eliminates variables from maximal depth toward
the root. Each nonroot vertex $v$ has a budget $A(v)$ satisfying
$$\sum_y I_v(x,y)\le A(v),$$ while the root carries a pinned weight. The
theorem concludes $$\sum_X
  \left(\prod_{v\ne0}I_v(X_{p(v)},X_v)\right)
  w_0(X_0)
  \le
  \left(\prod_{v\ne0}A(v)\right)
  \sum_y w_0(y).$$ The proof is an induction that removes a
maximal-level leaf and reindexes the remaining assignments. The
vertex-dependent form matters: the budget at $v$ depends on $c_T(v)$.

## Fixed-tree bound

For a fixed tree $T$, set $$A(v)=c_T(v)!\,M^{c_T(v)+1}.$$ The [normalized child estimate](04-moment-kernels.md#why-normalization-by-the-parent-metric-is-necessary) supplies $A(v)$ for every nonroot vertex. The [rooted moment estimate](04-moment-kernels.md#hard-core-moment-kernel) supplies the same
factorial-moment factor at the root. Therefore

<div id="prop:fixed-tree" class="proposition" markdown="1">

**Proposition 3** (Fixed-tree marked-root estimate). *For every fixed
complete-graph spanning tree $T$, $$\mathsf F_T(r)
  \le
  \left(\prod_{v=0}^{n}c_T(v)!\right)
  M^{2n+1}.$$*

</div>

<div class="proof" markdown="1">

*Exponent audit.* Every vertex contributes $M^{c_T(v)+1}$. Using the [child-count identity](03-rooted-tree-profile.md#child-count-profiles),
$$\sum_{v=0}^{n}(c_T(v)+1)=n+(n+1)=2n+1.$$ Hence the total moment power
is exactly $M^{2n+1}$. The formal proof separately establishes the
factorial product, power product, and exponent sum before recombining
them. ◻

</div>
