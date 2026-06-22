# Lean Rooted-Tree Polymer Expansion

**Machine-checked target-preserving Ursell leaf summation for polymer systems with holes.**

[Read the article](paper/index.md){ .md-button .md-button--primary }
[Read it as one page](generated/full-article.md){ .md-button }
[Inspect the Lean theorems](formalization/index.md){ .md-button }
[Reproduce the build](artifact/reproducibility.md){ .md-button }

![Target-preserving rooted-tree proof pipeline](assets/images/proof-pipeline.png)

<div class="grid cards" markdown>

-   **Integrated article**

    ---

    The manuscript, theorem map, references, and limitations are maintained in
    the same versioned documentation tree.

    [:octicons-arrow-right-24: Start reading](paper/index.md)

-   **Lean 4 companion**

    ---

    Three stable public theorem names re-export exact proofs from one immutable
    upstream revision.

    [:octicons-arrow-right-24: Formalization map](formalization/index.md)

-   **Auditable claims boundary**

    ---

    The site separates what the kernel checks from the model-specific and
    continuum statements that remain outside the artifact.

    [:octicons-arrow-right-24: Claims and scope](about/claims.md)

-   **Reproducible release**

    ---

    Committed dependency locks, static audits, deterministic ZIP generation,
    checksums, provenance attestation, and an SPDX SBOM support evaluation.

    [:octicons-arrow-right-24: Reproduce it](artifact/reproducibility.md)

</div>

## Result at a glance

For complete-graph spanning trees on `n+1` labelled vertices, rooted at `0`,
with rooted child counts $c_T(v)$,

$$
\frac{n+1}{(n+1)!}
\sum_T \prod_v c_T(v)! \le 4^n.
$$

Let $M$ be the rooted hard-core metric-moment constant and define $L=4M^2$.
The marked-root leaf sum obeys

$$
(n+1)S_n(r)\le M L^n,
$$

and preserving the exact target union until decay is extracted gives

$$
T_n(Y)\le M e^{-\rho m(Y)}L^n.
$$

## Public theorem interface

```lean
MarkedRootedClosure.normalizedRootedChildFactorialTreeBound
MarkedRootedClosure.markedRootLeafGeometricBound
MarkedRootedClosure.targetPreservingWeightedTreeBound
```

Each alias is an exact application of a theorem in the pinned upstream proof
development. See the [endpoint table](formalization/index.md) and the
[machine-readable theorem manifest](artifact/theorem-map.md).

## Trust boundary

This repository proves finite combinatorics and target-sensitive geometric
composition. It does not prove a model-specific raw Yang--Mills activity,
`hRpoly`, a continuum limit, reconstruction, or a mass gap. That distinction is
part of the artifact, not a footnote: see [Claims and scope](about/claims.md).

## Why the public name should change

The present slug `marked-rooted-closure` is compact but opaque. The recommended
rename is **`lean-rooted-tree-polymer-expansion`**, which names the formal
method, the mathematical object, and the implementation language. See the
[rename proposal](maintainers/rename-repository.md).
