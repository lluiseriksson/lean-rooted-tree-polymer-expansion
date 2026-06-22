# Marked Rooted-Tree Summation for Polymer Cluster Expansions with Holes

## A Lean 4 formalization

**Lluis Eriksson · June 2026**

!!! abstract "Abstract"
    We present a machine-checked finite mechanism for obtaining target-sensitive
    geometric bounds in a second Ursell expansion of a hard-core polymer gas
    with holes. The proof must preserve the exact target union long enough to
    extract modified-metric decay, while also preserving parent--child
    incompatibility data long enough to perform a local leaf recursion. Its
    principal ingredients are a normalized aggregate bound on rooted
    child-factorial tree weights, a parent-normalized incompatibility kernel,
    a marked-root bottom-up fixed-tree summation, and a target-preserving
    composition theorem. If `M` is the geometric moment constant, the verified
    orderwise estimates are

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

![Proof pipeline](../assets/images/proof-pipeline.png)

## Read the article

1. [Introduction](01-introduction.md)
2. [Polymer systems with holes](02-polymer-systems.md)
3. [The rooted tree-profile bound](03-rooted-tree-profile.md)
4. [Parent-normalized moment kernels](04-moment-kernels.md)
5. [Fixed-tree leaf elimination](05-fixed-tree-elimination.md)
6. [Marked-root geometric closure](06-marked-root-closure.md)
7. [Target-preserving decay](07-target-preserving-decay.md)
8. [Lean formalization](08-lean-formalization.md)
9. [Mathematical interpretation](09-interpretation.md)
10. [Related work and novelty boundary](10-related-work.md)
11. [Limitations and open obligations](11-limitations.md)
12. [Reproducibility](12-reproducibility.md)
13. [Conclusion](13-conclusion.md)
14. [References](references.md)

### Appendices

- [Public theorem signatures](appendix-a-signatures.md)
- [Constant audit](appendix-b-constants.md)
- [Reviewer checklist](appendix-c-reviewer-checklist.md)

## Immutable source state

The Lean companion depends on `THE-ERIKSSON-PROGRAMME` at commit
`4e45246aa109671d25fcd01ba1abf7bc3f8506d1`, with Lean
`v4.29.0-rc6` and Mathlib commit
`07642720480157414db592fa85b626dafb71355b`. The exact lock is recorded
in [`archive/UPSTREAM.lock`](https://github.com/lluiseriksson/marked-rooted-closure/blob/main/archive/UPSTREAM.lock).
