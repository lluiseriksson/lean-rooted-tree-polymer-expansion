# Artifact evaluation guide

## Claims to check

1. The Lean project resolves to the exact upstream and Mathlib commits.
2. `lake build MarkedRootedClosure` succeeds.
3. `MarkedRootedClosure/Oracle.lean` reports no project axiom or placeholder.
4. The three public theorem statements match the equations in the paper.
5. `paper/main.pdf` is reproducible from `paper/main.tex` and
   `paper/references.bib`.

## Suggested 15-minute review

```bash
cat archive/UPSTREAM.lock
sed -n '1,240p' MarkedRootedClosure/PaperTheorems.lean
lake build MarkedRootedClosure
lake env lean MarkedRootedClosure/Oracle.lean
```

Then compare the signatures with Sections 3--6 and Appendix A of the paper.

## Suggested deep review

Inspect the pinned upstream implementations named in `docs/THEOREM_MAP.md`, in
particular:

- the parent-profile counting argument;
- the parent-product cancellation identity;
- the vertexwise walk bound;
- the hard-core metric moment kernel;
- the order of target extraction and marked-root enlargement.
