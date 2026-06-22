# Polymer systems with holes

We record the finite structure abstracted by the Lean development. The
notation is chosen to expose the proof rather than reproduce every
implementation type.

## Active skeleton and full target

Let $\Lambda$ be a finite periodic lattice and let $\mathcal H$ be a
finite family of hole regions. A polymer $Q$ carries a full support
$|Q|\subseteq\Lambda$ and an active skeleton
$$\operatorname{skel}_{\mathcal H}(Q)\subseteq |Q|.$$ Hard-core
incompatibility is determined by active intersection, $$Q\not\sim Q'
  \quad\Longleftrightarrow\quad
  \operatorname{skel}_{\mathcal H}(Q)\cap\operatorname{skel}_{\mathcal H}(Q')\ne\varnothing.$$
The full support and active skeleton play different roles. The skeleton
controls connectivity and local incompatibility summation; the full
union labels the target activity.

For a tuple $\mathbf Q=(Q_0,\dots,Q_n)$, write
$$U(\mathbf Q)=\bigcup_{i=0}^{n}|Q_i|.$$ The exact target fiber over $Y$
is $$\mathfrak F_n(Y)
  =\{\mathbf Q:U(\mathbf Q)=Y\}.$$ The exact equality $U(\mathbf Q)=Y$
is the geometric information that must not be forgotten before target
decay is extracted.

## Modified metric and shifted size

Let $d_M(Q)$ denote the modified metric associated with the hole
geometry, and define the strictly positive shifted size
$$m(Q)=d_M(Q)+1.$$ The corresponding exponential weight is
$$\mathsf E_\rho(Q)=e^{-\rho m(Q)}.$$ The finite geometry provides a
stitching inequality of the form $$m(Y)\le \sum_{i=0}^{n}m(Q_i)
  \qquad
  \text{whenever }U(\mathbf Q)=Y
  \text{ and the tuple is incompatibility-connected.}$$ Consequently,
for $\rho\ge0$, $$\prod_{i=0}^{n}\mathsf E_\rho(Q_i)
  \le \mathsf E_\rho(Y).$$

## Second Ursell tree term

For a tuple $\mathbf Q$, let $G(\mathbf Q)$ be its incompatibility graph
on $\{0,\dots,n\}$. A nonnegative weighted tree term with exact target
$Y$ has the schematic form $$\mathsf T_n^w(Y)
  =\frac{1}{(n+1)!}
  \sum_{\mathbf Q\in\mathfrak F_n(Y)}
  \sum_{T\in\mathcal T(G(\mathbf Q))}
  \prod_{i=0}^{n}w(Q_i).$$ The formalized object uses the precise finite
polymer carrier and spanning-tree predicate. The nonnegative form is a
majorant for the absolute Ursell coefficient after a tree-graph step.
