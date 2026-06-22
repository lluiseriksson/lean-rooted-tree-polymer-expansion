# Target-preserving decay

The marked-root theorem is not yet target-sensitive: $Y$ has
disappeared. The target-preserving composition theorem ensures that it
disappears only after paying for its decay.

## Weight splitting

Let $w,u\ge0$ be weights satisfying $$w(Q)\le \mathsf E_\rho(Q)\,u(Q),
  \qquad \rho\ge0.$$ For each tuple in the exact target fiber, the [stitching inequality](02-polymer-systems.md#modified-metric-and-shifted-size) gives
$$\prod_{i=0}^{n}w(Q_i)
  \le
  \mathsf E_\rho(Y)\prod_{i=0}^{n}u(Q_i).$$ Thus
$$\mathsf T_n^w(Y)
  \le
  \mathsf E_\rho(Y)\,\mathsf T_n^u(Y).$$ Only now do we choose
$r\in\operatorname{skel}(Y)$ and enlarge the exact target fiber to the
marked-root sum.

<div id="thm:target" class="theorem" markdown="1">

**Theorem 5** (Target-preserving weighted-tree bound). *Assume the weight split above, assume
$u(Q)\le\mathsf E_{2\kappa_0}(Q)$, and assume
$r\in\operatorname{skel}(Y)$. Under the finite hole-geometry hypotheses,
$$\mathsf T_n^w(Y)
  \le
  M\,\mathsf E_\rho(Y)\,(4M^2)^n.$$*

</div>

<div class="proof" markdown="1">

*Proof.* The exact-target estimate above extracts the target factor. The fixed-union term for $u$ is at most
$(n+1)\mathsf S_n(r)$ because every tuple with union $Y$ contains the
marked cube in at least one coordinate, and a coordinate permutation
moves it to position $0$.
The [marked-root theorem](06-marked-root-closure.md) closes the remaining sum. ◻

</div>

<div id="rem:forbidden-order" class="remark" markdown="1">

**Remark 6** (The forbidden proof order). *If one first replaces the
exact-union fiber by a global marked-root sum, the resulting object no
longer contains $Y$. A bound with $e^{-\rho m(Y)}$ cannot then be
derived from that object alone. Reintroducing target decay as a
hypothesis would be circular. This failure mode is encoded in the
theorem architecture: target extraction and leaf summation are separate
theorems, and the former is applied first.*

</div>

## Geometric order sum

Suppose a model-specific activity estimate contributes a factor
$\varepsilon^{n+1}$ at order $n$. Then the target-preserving theorem yields
$$\varepsilon^{n+1}\mathsf T_n^w(Y)
  \le
  M\varepsilon\,\mathsf E_\rho(Y)
  (4M^2\varepsilon)^n.$$ Hence the following consequence is immediate.

<div id="cor:geometric" class="corollary" markdown="1">

**Corollary 7** (Closed geometric majorant). *If $4M^2\varepsilon<1$,
then $$\sum_{n=0}^{\infty}
  \varepsilon^{n+1}\mathsf T_n^w(Y)
  \le
  \frac{M\varepsilon}{1-4M^2\varepsilon}
  \mathsf E_\rho(Y).$$*

</div>

The corollary is a standard geometric-series calculation. The formal
contribution of the present work is the finite orderwise input with the
correct target factor and an explicit ratio.
