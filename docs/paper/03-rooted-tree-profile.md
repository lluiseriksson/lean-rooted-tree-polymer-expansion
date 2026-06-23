# The rooted tree-profile bound

The leaf recursion assigns a factorial cost to each rooted child count.
This section explains how those costs are summed over all labelled
complete-graph spanning trees.

## Child-count profiles

Root every tree $T$ on $\{0,\dots,n\}$ at $0$. Let
$$c_T(v)=\#\{u:\operatorname{parent}_T(u)=v\}$$ be the number of rooted
children of $v$. Then $$\sum_{v=0}^{n}c_T(v)=n.$$ The key weighted tree sum is
$$A_n=\sum_{T\in\mathcal T_{n+1}}\prod_{v=0}^{n}c_T(v)!.$$

A direct Cayley count is not the proof used in the artifact. Instead,
the tree is injected into its parent map on the $n$ nonroot labels.
Parent maps are grouped by the profile $$\mathbf c=(c(0),\dots,c(n)),
  \qquad c(v)\in\mathbb N,
  \qquad \sum_v c(v)=n.$$ For a fixed profile, the product
$\prod_v c(v)!$ pays for the permutations within the parent fibers. The
total fixed-profile cost is bounded by a single global $n!$ factor. The
number of weak compositions of $n$ into $n+1$ parts is
$$\binom{2n}{n}\le4^n.$$ This gives $A_n\le n!4^n$.

<div id="thm:tree-profile" class="theorem" markdown="1">

**Theorem 1** (Normalized rooted child-factorial tree bound). *For every
$n\in\mathbb N$, $$\frac{n+1}{(n+1)!}
  \sum_{T\in\mathcal T_{n+1}}
  \prod_{v=0}^{n}c_T(v)!
  \le4^n.$$*

</div>

!!! tip "Machine-checked endpoint"
    `MarkedRootedClosure.normalizedRootedChildFactorialTreeBound`

<div class="proof" markdown="1">

*Proof architecture.* The formal proof performs the following finite
steps.

1.  Encode each rooted tree by the BFS parent map on the nonroot labels
    and prove injectivity on spanning trees.

2.  Partition parent maps by their child-count profile.

3.  For a fixed profile, encode a fiber family together with local
    permutations into a global permutation of $n$ labels. This proves
    that the number of fiber families times $\prod_v c(v)!$ is at most
    $n!$.

4.  Count profiles by a finite antidiagonal, identify the count with
    $\binom{2n}{n}$, and use $\binom{2n}{n}\le4^n$.

5.  Cast the natural-number inequality to $\mathbb R$ and simplify
    $$\frac{n+1}{(n+1)!}\,n!=1.$$

Every step is a theorem in the pinned Lean source; no asymptotic
estimate is used. ◻

</div>

<div class="remark" markdown="1">

**Remark 2** (Central-binomial refinement). *The development also
retains the sharper intermediate bound with $\binom{2n}{n}$ visible. The
published geometric closure uses $4^n$ because it composes transparently
with the moment constant. An exact Catalan improvement would require
additional rooted plane-tree structure; it is not claimed here.*

</div>
