# Artifact evaluation guide

## Claims to check

1. Lake resolves to the exact upstream and Mathlib commits.
2. `lake build MarkedRootedClosure` succeeds.
3. The oracle reports no project axiom or placeholder.
4. The three public theorem statements match the integrated paper.
5. `mkdocs build --strict` succeeds and all internal links resolve.
6. No standalone paper PDF or duplicate manuscript source remains in the
   release tree.

## Suggested 15-minute review

```bash
cat archive/UPSTREAM.lock
sed -n '1,260p' MarkedRootedClosure/PaperTheorems.lean
lake build MarkedRootedClosure
lake env lean MarkedRootedClosure/Oracle.lean
python3 scripts/check_artifact.py
```

Then compare the compiled signatures with the [theorem map](theorem-map.md) and
paper Sections 3--7.

## Suggested deep review

Inspect the pinned upstream implementations of:

- the parent-profile counting argument;
- the parent-product cancellation identity;
- the vertexwise walk bound;
- the hard-core metric-moment kernel;
- the order of target extraction and marked-root enlargement.
