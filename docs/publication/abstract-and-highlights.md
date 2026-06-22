# Abstract and highlights

## Submission abstract

We present a machine-checked finite mechanism for obtaining target-sensitive
geometric bounds in a second Ursell expansion of a hard-core polymer gas with
holes. The proof must preserve the exact target union long enough to extract
modified-metric decay, while retaining parent--child incompatibility data long
enough to perform a local leaf recursion. In Lean 4 we formalize a normalized
aggregate bound on rooted child-factorial tree weights, a parent-normalized
incompatibility kernel, a marked-root bottom-up fixed-tree summation, and a
target-preserving composition theorem. If `M` denotes the geometric moment
constant, the verified estimates are `(n+1) S_n(r) <= M (4 M^2)^n` and
`T_n(Y) <= M exp(-rho m(Y)) (4 M^2)^n`. The result is finite and orderwise; it
does not prove the model-specific raw Yang--Mills activity estimate, a continuum
limit, or a mass gap. The complete article, Lean interface, theorem map, source
locks, and evaluation instructions are maintained as one documentation site.

## Highlights

- Formalizes a target-preserving second-Ursell leaf-summation mechanism.
- Proves a normalized `4^n` bound for rooted child-factorial tree weights.
- Uses parent-metric normalization to close local hard-core child moments.
- Keeps exact target geometry until exponential decay has been extracted.
- Ships a pinned Lean companion and strict reproducibility/evaluation workflow.
