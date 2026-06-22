# Marked Rooted-Tree Summation for Polymer Cluster Expansions with Holes

## A Lean 4 formalization

**Lluis Eriksson · June 2026**

[Read section by section](00-reader-guide.md){ .md-button .md-button--primary }
[Read the generated full article](../generated/full-article.md){ .md-button }
[Inspect the theorem map](../formalization/index.md){ .md-button }

!!! abstract "Abstract"
    We present a machine-checked finite mechanism for obtaining
    target-sensitive geometric bounds in a second Ursell expansion of a
    hard-core polymer gas with holes. The proof must preserve the exact target
    union long enough to extract modified-metric decay, while also preserving
    parent--child incompatibility data long enough to perform a local leaf
    recursion. Its principal ingredients are a normalized aggregate bound on
    rooted child-factorial tree weights, a parent-normalized incompatibility
    kernel, a marked-root bottom-up fixed-tree summation, and a
    target-preserving composition theorem. If $M$ is the geometric moment
    constant, the verified orderwise estimates are

    $$
    (n+1)S_n(r) \le M(4M^2)^n
    $$

    and

    $$
    T_n(Y) \le M e^{-\rho m(Y)}(4M^2)^n.
    $$

    The result is finite, combinatorial, and geometric. It does not prove the
    model-specific raw Yang--Mills activity estimate, a continuum limit, or a
    mass gap.

**Keywords:** Lean 4; cluster expansion; polymer model; Ursell function;
rooted tree; modified metric; renormalization group; constructive field theory.

![Target-preserving proof pipeline](../assets/images/proof-pipeline.png)

## Verified statements

| Result | Paper form | Lean endpoint |
|---|---|---|
| Rooted tree-profile bound | $\frac{n+1}{(n+1)!}\sum_T\prod_v c_T(v)!\le4^n$ | `normalizedRootedChildFactorialTreeBound` |
| Marked-root leaf closure | $(n+1)S_n(r)\le M(4M^2)^n$ | `markedRootLeafGeometricBound` |
| Exact-target composition | $T_n(Y)\le M e^{-\rho m(Y)}(4M^2)^n$ | `targetPreservingWeightedTreeBound` |

The table is only a readable synopsis. The complete typed hypotheses are in the
[public theorem signatures](appendix-a-signatures.md) and
[`MarkedRootedClosure/PaperTheorems.lean`](https://github.com/lluiseriksson/lean-rooted-tree-polymer-expansion/blob/main/MarkedRootedClosure/PaperTheorems.lean).

## Article contents

1. [Reader guide and proof architecture](00-reader-guide.md)
2. [Introduction](01-introduction.md)
3. [Polymer systems with holes](02-polymer-systems.md)
4. [The rooted tree-profile bound](03-rooted-tree-profile.md)
5. [Parent-normalized moment kernels](04-moment-kernels.md)
6. [Fixed-tree leaf elimination](05-fixed-tree-elimination.md)
7. [Marked-root geometric closure](06-marked-root-closure.md)
8. [Target-preserving decay](07-target-preserving-decay.md)
9. [Lean formalization](08-lean-formalization.md)
10. [Mathematical interpretation](09-interpretation.md)
11. [Related work and novelty boundary](10-related-work.md)
12. [Limitations and open obligations](11-limitations.md)
13. [Reproducibility](12-reproducibility.md)
14. [Conclusion](13-conclusion.md)
15. [References](references.md)

### Appendices

- [Public theorem signatures](appendix-a-signatures.md)
- [Constant audit](appendix-b-constants.md)
- [Reviewer checklist](appendix-c-reviewer-checklist.md)

## Immutable source state

The Lean companion depends on `THE-ERIKSSON-PROGRAMME` at commit
`4e45246aa109671d25fcd01ba1abf7bc3f8506d1`, with Lean `v4.29.0-rc6` and
Mathlib commit `07642720480157414db592fa85b626dafb71355b`. The exact lock is
recorded in
[`archive/UPSTREAM.lock`](https://github.com/lluiseriksson/lean-rooted-tree-polymer-expansion/blob/main/archive/UPSTREAM.lock)
and [`lake-manifest.json`](https://github.com/lluiseriksson/lean-rooted-tree-polymer-expansion/blob/main/lake-manifest.json).
