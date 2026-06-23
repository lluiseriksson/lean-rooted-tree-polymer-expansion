# Agent instructions

1. Preserve the three public theorem statements and immutable upstream pin.
2. Treat `project.json`, `lake-manifest.json`, and
   `archive/theorem-manifest.json` as release-critical files.
3. Run `make static` after documentation, metadata, URL, or packaging changes.
4. Run `make verify-nonlean` locally and require the green GitHub Actions Lean
   gate before tagging. A local Lean run is supporting evidence, not a
   substitute for the expected cached Linux CI environment.
5. Use `make lean`, `make lean-build`, or `make lean-oracle` for long local
   Lean/Lake work. Do not wrap raw Lean commands in an external timeout that can
   orphan descendants, and never kill unrelated system processes.
6. Never introduce `sorry`, `admit`, `sorryAx`, or project-local axioms.
7. Do not claim a Yang--Mills mass gap, `hRpoly`, continuum construction,
   reconstruction theorem, cardinal-infinity theorem, or Riemann-hypothesis
   result.
8. Keep the canonical paper sections under `docs/paper/`; do not add a tracked
   manuscript PDF or a second manually edited full-paper source.
9. The page `docs/generated/full-article.md` is generated. Edit the canonical
   sections and `docs/paper/manifest.json` instead.
10. Refresh dependency locks only with `make lock-refresh`, in a dedicated
    change whose diff is reviewed.
11. A repository rename changes URLs and release names only. Keep the stable
    Lean namespace `MarkedRootedClosure` unless a separately versioned API
    migration is explicitly approved.
12. After any distributable source change, run `make manifest` and review the
    `MANIFEST.sha256` diff before `make static`.
13. Keep `docs/llms.txt` synchronized with project metadata, verification
    entrypoints, and the three public theorem endpoints.
14. Keep release publication privilege-separated and exact-set based. Do not
    execute repository code in the privileged publish job or replace the 13
    explicit assets with shell globs.
