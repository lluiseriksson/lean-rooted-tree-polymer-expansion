# Conclusion

The formal result can be summarized in one sentence: *extract target
decay while the exact union is still present, then mark a root and sum
the remaining tree locally*. That proof order produces the explicit
finite bound $$\mathsf T_n(Y)
  \le
  M\,e^{-\rho m(Y)}(4M^2)^n,$$ with every combinatorial and geometric
factor exposed. Lean 4 verifies the parent-profile count, metric
cancellation, leaf recursion, root moment, tree sum, and target
composition as separate reusable theorems.

The artifact is deliberately narrower than the larger constructive
field-theory programme that motivated it. That narrowness is a strength:
the statement can be audited, rebuilt, cited, and reused without
confusing a finite cluster-expansion theorem with the still-open
model-specific and continuum analysis.
