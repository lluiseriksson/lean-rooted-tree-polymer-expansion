# Lean formalization

## Pinned environment

The artifact is a small publication companion around a pinned, larger
formalization repository. Its locked environment is shown below.

<div id="tab:versions">

| Component               | Locked value                               |
|:------------------------|:-------------------------------------------|
| Lean                    | `leanprover/lean4:v4.29.0-rc6`             |
| Mathlib                 | `07642720480157414db592fa85b626dafb71355b` |
| Upstream repository     | `lluiseriksson/THE-ERIKSSON-PROGRAMME`     |
| Upstream commit         | `4e45246aa109671d25fcd01ba1abf7bc3f8506d1` |

Pinned software and upstream source state. Exact file paths and theorem names are recorded in the theorem manifest and provenance pages.

</div>

The companion module gives stable, paper-facing names to three upstream
theorems. It adds no axiom and no opaque mathematical field.

## Publication-facing endpoints

The first endpoint is an exact alias of the [rooted tree-profile theorem](03-rooted-tree-profile.md).

```
theorem normalizedRootedChildFactorialTreeBound (n : Nat) :
    ((n : Real) + 1) *
        (((n + 1).factorial : Real))^-1 *
        (sum T in spanningTrees (top : SimpleGraph (Fin (n + 1))),
          prod v : Fin (n + 1),
            ((rootedChildCount T v).factorial : Real))
      <= (4 : Real)^n
```

The marked-root endpoint retains every finite geometric hypothesis of the [marked-root theorem](06-marked-root-closure.md); in particular, the hole
conditions and the numerical summability condition are visible. The
target endpoint similarly exposes $w$, $u$, the split inequality, the
target root, and the residual rate.

```
theorem targetPreservingWeightedTreeBound
    ...
    (hsplit : forall Q,
      w Q <= appendixFHoleExpWeight HF rate Q.val * u Q)
    (hu_exp : forall Q,
      u Q <= appendixFHoleExpWeight HF (2 * kappa0) Q.val)
    (hr : r in skeleton HF Y)
    ... :
    appendixFHoleHsharpWeightedTreeTerm HF zK w Y n <=
      appendixFSecondUrsellMomentConstant d kappa0 *
        appendixFHoleExpWeight HF rate Y *
        appendixFSecondUrsellLeafConstant d kappa0 ^ n
```

## Theorem dependency map

The machine-checked dependency ladder is $$\begin{gathered}
\text{parent-map fibers}\to\text{fixed-profile factorial budget}\\
\to\text{central-binomial profile count}\to\text{normalized }4^n\text{ bound}\\
\to\text{parent-product cancellation}\to\text{normalized child kernel}\\
\to\text{vertexwise tree walk}\to\text{fixed-tree moment bound}\\
\to\text{marked-root geometric bound}\to\text{target extraction}\\
\to\text{target-preserving orderwise bound}.
\end{gathered}$$ The [theorem map](../artifact/theorem-map.md) gives a one-line map from each paper theorem to the exact upstream theorem and file.

## Proof trust and oracle

The build target compiles the companion module and then invokes Lean on
an oracle file containing `#print axioms` for the public endpoints. The
expected output is limited to standard classical principles inherited
from Mathlib and the pinned core, normally
$$[\texttt{propext},\ \texttt{Classical.choice},\ \texttt{Quot.sound}].$$
Static checks reject `sorry`, `admit`, and project-local `axiom`
declarations in the companion source. The CI workflow separately builds this documentation site in strict mode; the paper is part of the site rather than a standalone PDF artifact.
