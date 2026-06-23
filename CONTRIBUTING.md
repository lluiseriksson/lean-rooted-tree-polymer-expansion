# Contributing

Contributions are welcome when they preserve the artifact's mathematical,
publication, and reproducibility boundaries.

## Required checks

```bash
make verify-nonlean
```

GitHub Actions performs the authoritative single Lean build and exact oracle.
For deliberate local supporting evidence, use `make lean`; its supervisor
cleans the complete Lean/Lake process tree on timeout or interruption.

A theorem change must include:

1. a Lean proof without `sorry`, `admit`, `sorryAx`, or a new project-local
   axiom;
2. an oracle update;
3. a theorem-manifest and theorem-map update;
4. an article update if the public statement or interpretation changes;
5. a clean CI run from the pinned environment.

Documentation changes must edit the canonical pages under `docs/`, keep
`docs/paper/manifest.json` consistent, and pass the strict site and link audits.
Do not edit `docs/generated/full-article.md`; it is rebuilt from the section
sources.

## Dependency changes

Do not run `lake update` as incidental cleanup. Dependency revisions require a
dedicated pull request, an explicit `make lock-refresh`, review of the complete
manifest diff, and renewed oracle and clean-cache CI checks.

## Claims discipline

Model-specific Yang--Mills assumptions must remain explicit and must not be
renamed as if proved by the finite combinatorial layer. Novelty language should
remain qualified unless supported by a fresh literature review.

## Repository identity

Public URLs are checked against `project.json`. After an actual GitHub rename,
use `scripts/rename_repository.py` rather than editing a subset of files by
hand. The stable Lean namespace is intentionally independent of the repository
slug.

## Pull requests

Keep changes focused. Explain which theorem, page, metadata field, or
reproducibility property changes and include the exact commands and environment
used for verification.
