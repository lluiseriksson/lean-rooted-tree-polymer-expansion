# Novelty and scope

## Claim made

The artifact gives a machine-checked, end-to-end implementation of a finite
mechanism used in polymer cluster expansions with holes:

1. root a labelled spanning tree;
2. expose child-count factorials;
3. sum fixed profiles with a global permutation budget;
4. control profile entropy by the central binomial coefficient and `4^n`;
5. normalize child kernels by the parent metric;
6. eliminate leaves bottom-up using factorial moment estimates;
7. retain the exact target union until modified-metric decay is extracted;
8. obtain a target-sensitive geometric order bound.

A targeted literature search found the classical tree-graph and polymer
expansion sources and recent Lean formalizations of quantum field theory, but no
prior public Lean artifact for this specific target-preserving Appendix-F leaf
summation pipeline. The wording remains **to the best of our knowledge**; no
universal priority claim is made.

## Inherited mathematics

The mathematical strategy belongs to classical tree-graph expansions,
Kotecký--Preiss-type polymer estimates, and the Balaban--Dimock
renormalization-group literature. The contribution is the formal decomposition,
constant tracking, target-preserving proof order, stable theorem interface, and
reproducible machine-checked assembly.

## Not claimed

The repository does not prove:

- the concrete raw activity estimate for four-dimensional Yang--Mills;
- the source translation from Balaban CMP116 to a concrete Lean activity;
- `hRpoly` without model-specific analytic inputs;
- a continuum limit or physical mass gap;
- a new cardinality result about infinity;
- a relation to the Riemann hypothesis.
