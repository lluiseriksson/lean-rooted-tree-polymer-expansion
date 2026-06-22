# Proposed repository name

## Recommended slug

```text
lean-rooted-tree-polymer-expansion
```

## Recommended public URL

```text
https://lluiseriksson.github.io/lean-rooted-tree-polymer-expansion/
```

This name is more discoverable than `marked-rooted-closure`: it identifies the
Lean implementation, the rooted-tree method, and the polymer-expansion domain.
The manuscript title and the stable Lean namespace `MarkedRootedClosure` should
remain unchanged.

The complete rationale and migration checklist are documented at
[`docs/maintainers/rename-repository.md`](docs/maintainers/rename-repository.md).
After the GitHub repository itself has been renamed, run:

```bash
python3 scripts/rename_repository.py \
  --owner lluiseriksson \
  --slug lean-rooted-tree-polymer-expansion \
  --apply
make static
```
