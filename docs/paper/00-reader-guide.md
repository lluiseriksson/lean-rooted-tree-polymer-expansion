# Reader guide and proof architecture

This article isolates one finite mechanism inside a larger constructive
renormalization-group programme. A reader can evaluate the result at three
levels.

## Three reading paths

**Mathematical path.** Read Sections 2--7 for the polymer geometry, rooted-tree
profile estimate, normalized moment kernel, fixed-tree recursion, and exact
target composition.

**Formalization path.** Read Section 8 together with the
[formalization map](../formalization/index.md) and the three short aliases in
`MarkedRootedClosure/PaperTheorems.lean`.

**Artifact path.** Read Section 12 and the
[reproducibility guide](../artifact/reproducibility.md), then run `make verify-nonlean`; inspect the green GitHub Actions Lean gate separately.

## Main logical chain

The proof is organized around the following information flow:

$$
\begin{aligned}
&\text{finite hard-core moment estimate}
\\[-1mm]
&\quad\Downarrow
\\[-1mm]
&\text{parent-normalized child kernel}
\\[-1mm]
&\quad\Downarrow
\\[-1mm]
&\text{fixed-tree bottom-up elimination}
\\[-1mm]
&\quad\Downarrow
\\[-1mm]
&\prod_v c_T(v)!\,M^{2n+1}
\\[-1mm]
&\quad\Downarrow\quad
\frac{n+1}{(n+1)!}\sum_T\prod_v c_T(v)!\le4^n
\\[-1mm]
&\text{marked-root bound }(n+1)S_n(r)\le M(4M^2)^n
\\[-1mm]
&\quad\Downarrow
\\[-1mm]
&\text{exact-target bound }T_n(Y)\le
M e^{-\rho m(Y)}(4M^2)^n.
\end{aligned}
$$

The exact target union is retained until the exponential factor has been
extracted. Parent-edge incompatibility is retained until the local leaf sum has
been performed. These are the two non-negotiable ordering constraints.

## Theorems versus corollaries

The Lean API exposes finite orderwise statements. The infinite geometric
series used in interpretation is an ordinary analytic corollary under
$4M^2\varepsilon<1$; it is not presented as an additional model-specific
activity theorem.

## Claims boundary

The result does not construct the raw gauge activity, take a continuum limit,
or prove a mass gap. Section 11 and the standalone
[claims page](../about/claims.md) list the excluded statements explicitly.
