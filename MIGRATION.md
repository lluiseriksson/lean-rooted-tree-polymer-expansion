# Migration from v1.0.0

Version 2.0.0 changes the publication model from a separate LaTeX/PDF bundle to
an integrated documentation article.

## Removed

- `paper/` and its PDF/LaTeX duplicates;
- nested `release-artifacts/` copies;
- PDF-specific CI and preflight scripts.

## Added

- full article under `docs/paper/`;
- MkDocs Material configuration and strict docs build;
- GitHub Pages deployment;
- hardened metadata, governance, security, migration, and release checks;
- deterministic source-only release packaging;
- current immutable upstream pin.

Upload with `rsync --delete` or an equivalent replacement operation. Overlaying
the ZIP without deleting old paths defeats this migration.
