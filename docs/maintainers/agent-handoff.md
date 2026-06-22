# Publishing-agent handoff

## Mission

Replace the existing repository contents with this v2.0.0 tree, run the complete
verification workflow, deploy the integrated paper through GitHub Pages, and
publish an immutable source release without broadening the mathematical claims.

## Important migration

The previous repository tracked a standalone manuscript PDF, duplicate LaTeX sources, and nested
release artifacts. Version 2.0.0 intentionally removes them. The article now
lives under `docs/paper/` and is built by MkDocs. Use a **delete-aware** copy so
legacy files do not survive.

Recommended command from a clean clone:

```bash
rsync -a --delete --exclude='.git/' \
  /path/to/marked-rooted-closure-v2.0.0/ ./
git add -A
git commit -m "docs: integrate paper and harden publication artifact"
git push origin main
```

## Non-negotiable claims discipline

The headline result is finite and orderwise. Do not advertise it as a proof of
`hRpoly`, the Yang--Mills mass gap, a continuum limit, or a new theory of
cardinal infinity. Do not replace “to the best of our knowledge” by an
unconditional novelty claim.

## Publication gate

1. Clean-cache Lean CI is green.
2. The oracle shows only expected classical axioms.
3. Strict docs build is green.
4. Internal-link and artifact audits pass.
5. The deployed Pages site has been visually checked.
6. The release ZIP hash is recorded.
7. The DOI, if any, is inserted consistently.
8. A fresh literature search has been completed.

## Files whose consistency must be preserved

- `lakefile.lean`
- `lean-toolchain`
- `archive/UPSTREAM.lock`
- `archive/theorem-manifest.json`
- `MarkedRootedClosure/PaperTheorems.lean`
- `docs/artifact/theorem-map.md`
- the claims-boundary language throughout the paper
