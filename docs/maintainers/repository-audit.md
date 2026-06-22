# Repository audit for v2.1.0

**Audit date:** 2026-06-22  
**Current remote:** `lluiseriksson/lean-rooted-tree-polymer-expansion`  
**Audited base release:** v2.0.0 documentation-integrated tree

## Base state confirmed

The public repository exposes the integrated article, three stable Lean theorem
aliases, exact source locks, CI, GitHub Pages deployment, evaluator material,
and deterministic release tooling. The standalone PDF/LaTeX publication model
has already been removed.

## Gaps addressed by v2.1.0

1. The previously supplied v2.0.0 ZIP omitted `lake-manifest.json`, although the
   live repository tracked it. The new release archive requires and verifies
   that file.
2. Ordinary verification ran `lake update`, which could rewrite the committed
   dependency graph. Verification now consumes the manifest; lock refresh is a
   separate target.
3. The site name and repository slug did not explain the mathematical domain to
   a new reader. The site is now branded **Lean Rooted-Tree Polymer Expansion**,
   and a migration-safe descriptive slug is proposed.
4. The sectional article lacked a one-page reading view. A generated continuous
   view now derives from the same canonical sources.
5. Identity, paper order, Lake pins, oracle logs, and release determinism were
   not independently checked. Dedicated audits now cover each layer.
6. Release metadata did not include a software bill of materials. Packaging now
   emits SPDX 2.3 JSON and a checksum.
7. Maintainer guidance still described the pre-v2 migration as current work.
   The handoff and release playbook now describe the actual live state.

## Preserved mathematical interface

```text
MarkedRootedClosure.normalizedRootedChildFactorialTreeBound
MarkedRootedClosure.markedRootLeafGeometricBound
MarkedRootedClosure.targetPreservingWeightedTreeBound
```

No theorem statement or upstream proof revision is changed by this hardening
release.

## Remaining external gates

A package assembled outside a Lean-enabled, networked environment cannot by
itself certify a fresh kernel rebuild or GitHub Pages deployment. Those gates
remain explicit CI requirements before tagging.
