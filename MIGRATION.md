# Migration to v2.1.0

Version 2.1.0 is a publication-hardening release. It preserves the three Lean
theorem statements and the integrated-documentation model introduced in v2.0.0.

## Improvements over v2.0.0

- commits the authoritative `lake-manifest.json` in the release ZIP;
- removes `lake update` from ordinary verification and makes lock refresh
  explicit;
- adds a single-source continuous article generated from the canonical section
  files;
- adds project-identity, paper-manifest, Lake-lock, oracle-log, and deterministic
  release audits;
- adds an SPDX 2.3 JSON software bill of materials;
- clarifies the site identity and proposes the descriptive repository slug
  `lean-rooted-tree-polymer-expansion`;
- adds an idempotent repository-rename metadata tool;
- improves site navigation, print rendering, evaluator documentation, and the
  release playbook.

## Replacement procedure

Use a delete-aware copy so obsolete files from an earlier checkout do not
survive:

```bash
rsync -a --delete --exclude='.git/' \
  /path/to/lean-rooted-tree-polymer-expansion-v2.1.0/ ./
make static
```

Do not run the rename helper until the GitHub repository has actually been
renamed. The proposed rename is optional and does not change the Lean API.
