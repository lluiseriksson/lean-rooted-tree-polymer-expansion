# Contributing

Contributions are welcome when they preserve the artifact's mathematical and
reproducibility boundaries.

## Required checks

```bash
make static
make verify
```

A theorem change must include:

1. a Lean proof without `sorry`, `admit`, or a new project-local axiom;
2. an oracle update;
3. a theorem-manifest and theorem-map update;
4. a paper update if the public statement or interpretation changes;
5. a clean CI run from the pinned environment.

Documentation changes must keep the article under `docs/paper/` and pass
`mkdocs build --strict` plus the internal-link audit.

## Claims discipline

Model-specific Yang--Mills assumptions must remain explicit and must not be
renamed as if proved by the finite combinatorial layer. Novelty wording should
remain qualified unless supported by a fresh literature review.

## Pull requests

Keep pull requests focused. Explain which theorem, page, or reproducibility
property changes, and include the exact commands run. Do not update dependency
pins incidentally; pin updates require a dedicated pull request and renewed
oracle review.
