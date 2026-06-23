# Artifact evaluation guide

## Claims to check

1. Lake resolves to the exact upstream and Mathlib commits.
2. The GitHub Actions Lean job performs one explicit `MarkedRootedClosure` build.
3. The following `make lean-oracle` step reports no project axiom or placeholder.
4. The three public theorem statements match the integrated paper.
5. `mkdocs build --strict` succeeds and all internal links resolve.
6. No standalone paper PDF or duplicate manuscript source remains in the
   release tree.

## Suggested 15-minute review

```bash
cat archive/UPSTREAM.lock
sed -n '1,260p' MarkedRootedClosure/PaperTheorems.lean
make verify-nonlean
python3 scripts/check_artifact.py
```

Then compare the public signatures with the [theorem map](theorem-map.md) and
paper Sections 3--7, and inspect the final GitHub Actions Lean/oracle logs. A
maintainer performing an additional local kernel run should use `make lean`,
which supervises the complete process tree.

## Suggested deep review

Inspect the pinned upstream implementations of:

- the parent-profile counting argument;
- the parent-product cancellation identity;
- the vertexwise walk bound;
- the hard-core metric-moment kernel;
- the order of target extraction and marked-root enlargement.
