# Reproducibility

## One-command verification

```bash
make docs-setup
make verify
```

This target performs:

1. dependency resolution;
2. Lean compilation of the publication companion;
3. the axiom oracle;
4. strict documentation build;
5. source-lock, metadata, internal-link, and placeholder audits.

The equivalent explicit sequence is:

```bash
lake update
lake build MarkedRootedClosure
lake env lean MarkedRootedClosure/Oracle.lean
python3 -m pip install -r requirements-docs.txt
mkdocs build --strict
bash scripts/check_no_placeholders.sh
python3 scripts/check_artifact.py
python3 scripts/check_internal_links.py
```

## Container build

```bash
docker build -t marked-rooted-closure .
docker run --rm -v "$PWD:/workspace" -w /workspace \
  marked-rooted-closure make verify
```

## Expected oracle

The public endpoints should depend only on the standard classical principles
inherited from Mathlib and the pinned upstream core, normally:

```text
[propext, Classical.choice, Quot.sound]
```

No project-local axiom, `sorry`, or `admit` is accepted.

## Offline review

The repository itself contains the integrated paper, theorem signatures,
source lock, theorem manifest, and exact statement excerpts. A full first Lean
build still needs the pinned Git dependencies or a populated Lake cache. This
network requirement is explicit and is not described as an offline build.

## Deterministic release archive

For a source package after the static and documentation checks:

```bash
make package
```

For a publication release that reruns Lean first:

```bash
make release
```

The release script excludes caches and generated site output, normalizes ZIP
metadata, writes `MANIFEST.sha256`, and produces a versioned ZIP plus SHA-256
sidecar in `release/`.


The rendered graphical abstract is stored as a PNG for the site; its editable figure source is retained at `docs/assets/source/graphical-abstract.tex`.
