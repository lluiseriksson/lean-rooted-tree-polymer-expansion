# Reproducibility

## Locked inputs

| Component | Locked value |
|---|---|
| Lean | `leanprover/lean4:v4.29.0-rc6` |
| Upstream repository | `lluiseriksson/THE-ERIKSSON-PROGRAMME` |
| Upstream commit | `83d18a113e3fa22ada23b13361fb84015a1c80ed` |
| Upstream Mathlib commit | `07642720480157414db592fa85b626dafb71355b` |
| Rooted-tree source blob | `1415686403c26536da8736a9021237773c7467dc` |
| Appendix-F source blob | `0307d11b95d4385d4ea39067290e7eec929cd7f6` |

The same values are machine-readable in `archive/UPSTREAM.lock` and
`archive/theorem-manifest.json`.

## Clean build

```bash
git clone <this-repository>
cd marked-rooted-closure
lake update
lake build MarkedRootedClosure
lake env lean MarkedRootedClosure/Oracle.lean
make -C paper clean all
bash scripts/check_no_placeholders.sh
python3 scripts/check_artifact.py
```

Expected Lean oracle: only the standard classical axioms inherited from Mathlib
and the upstream core, normally `[propext, Classical.choice, Quot.sound]`.

## Offline review

The ZIP includes the paper PDF, theorem signatures, exact upstream hashes, and
short source excerpts.  A full kernel rebuild requires network access on first
run because Mathlib and the pinned upstream repository are Git dependencies.
After `lake update`, subsequent builds can be performed from the Lake cache.

## Releasing

```bash
make release
```

This creates a clean archive in `release/` after rebuilding the paper and
running the static artifact checks.
