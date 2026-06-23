# Migration to v2.4.0

Version 2.4.0 preserves the three public Lean theorem statements and the
integrated-documentation model. It replaces the v2.3 source tree to repair the
Python dependency environment and add proof-DAG, accessibility, safe-extraction,
and deterministic provenance evidence.

## Replacement procedure

Use a delete-aware copy so obsolete files and generated caches do not survive:

```bash
rsync -a --delete --exclude='.git/' \
  /path/to/lean-rooted-tree-polymer-expansion-v2.4.0/ ./
make docs-setup
make test
make syntax
make static
make docs
```

Then push without tagging and wait for the Lean, static/docs, package
reproducibility, clean-room, and Pages checks. Tag `v2.4.0` only after all
required checks are green.

## Important dependency change

Do not recreate the old `cffconvert`/`jsonschema` combination or reinstall the
direct-only requirements file in CI. All reproducible environments install:

```bash
python -m pip install -r requirements-docs.lock
```

`requirements-docs.txt` remains the reviewed four-package direct intent; the
lock is the executable transitive environment.

## Release evidence change

Tagged releases now include `*.intoto.jsonl` and its SHA-256 sidecar in
addition to the source ZIP, two SBOMs, build information, release index, and
aggregate checksum file.
