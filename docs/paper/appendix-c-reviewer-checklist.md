# Reviewer checklist

A reviewer can audit the central claim in the following order:

1.  Check `archive/UPSTREAM.lock` and the exact dependency SHA in
    `lakefile.lean`.

2.  Inspect the three wrapper statements in `PaperTheorems.lean`.

3.  Build `MarkedRootedClosure` and run the oracle file.

4.  Inspect the upstream implementations listed in
    [`docs/artifact/theorem-map.md`](../artifact/theorem-map.md).

5. Compare the three headline formulas in the paper with the compiled signatures.

6.  Confirm that the limitations paragraph remains unchanged in the
    abstract and conclusion.
