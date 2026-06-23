# Repository identity history

## Current identity

- Repository: `lluiseriksson/lean-rooted-tree-polymer-expansion`
- Pages: <https://lluiseriksson.github.io/lean-rooted-tree-polymer-expansion/>
- Lean package and namespace: `MarkedRootedClosure`

The descriptive public slug is adopted. It names the three externally visible
features of the artifact: Lean, rooted trees, and polymer expansions.

## Historical identity

The initial repository slug was `marked-rooted-closure`. It recorded an internal
proof phrase but was not self-explanatory to readers outside the source
programme. GitHub redirects ordinary repository URLs after a rename; the Pages
URL changed and is treated as a new public endpoint.

## Future identity migrations

Use the helper in dry-run mode first:

```bash
python3 scripts/rename_repository.py \
  --owner NEW_OWNER \
  --slug NEW_SLUG
```

After the repository has actually been renamed in GitHub Settings, apply the
changes and audit them:

```bash
python3 scripts/rename_repository.py \
  --owner NEW_OWNER \
  --slug NEW_SLUG \
  --apply
make test
make static
make docs
```

Do not rename the Lean package merely because the GitHub slug changes. A Lean
namespace migration is an independent API decision.
