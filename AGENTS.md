# Agent instructions

1. Preserve the three public theorem statements and immutable upstream pin.
2. Treat `project.json`, `lake-manifest.json`, and
   `archive/theorem-manifest.json` as release-critical files.
3. Run `make static` after documentation, metadata, URL, or packaging changes.
4. Run `make verify` and wait for green GitHub Actions before tagging.
5. Never introduce `sorry`, `admit`, `sorryAx`, or project-local axioms.
6. Do not claim a Yang--Mills mass gap, `hRpoly`, continuum construction,
   reconstruction theorem, cardinal-infinity theorem, or Riemann-hypothesis
   result.
7. Keep the canonical paper sections under `docs/paper/`; do not add a tracked
   manuscript PDF or a second manually edited full-paper source.
8. The page `docs/generated/full-article.md` is generated. Edit the canonical
   sections and `docs/paper/manifest.json` instead.
9. Refresh dependency locks only with `make lock-refresh`, in a dedicated
   change whose diff is reviewed.
10. A repository rename changes URLs and release names only. Keep the stable
    Lean namespace `MarkedRootedClosure` unless a separately versioned API
    migration is explicitly approved.

9. Keep `docs/llms.txt` synchronized with project metadata and the three public theorem endpoints.
