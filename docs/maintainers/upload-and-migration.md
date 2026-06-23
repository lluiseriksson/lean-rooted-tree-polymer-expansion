# Upload and migration instructions

Version 2.4.0 should replace the working tree, not be copied as a partial
overlay.

## Safe procedure

```bash
git clone https://github.com/lluiseriksson/lean-rooted-tree-polymer-expansion.git
cd lean-rooted-tree-polymer-expansion
rsync -a --delete --exclude='.git/' \
  /path/to/lean-rooted-tree-polymer-expansion-v2.4.0/ ./
make test
make static

git status --short
git add -A
git commit -m "release: harden traceability and release evidence v2.4.0"
git push origin main
```

The delete-aware copy is important: it removes the superseded
`REPOSITORY_RENAME.md` and `docs/maintainers/rename-repository.md` files.

## After the push

1. Wait for the `verify` and `documentation` workflows.
2. Confirm Lean, tooling tests, static/docs, deterministic package, and
   clean-room archive jobs are green.
3. Inspect the deployed site, including formulas, search, edit links, citation,
   verification contract, and continuous article.
4. Create tag `v2.4.0` only after all checks pass.
5. Confirm that the release includes the ZIP, all SHA-256 sidecars, SPDX SBOM,
   CycloneDX SBOM, build information, and provenance attestations.
6. Archive the verified release and update DOI metadata in a later commit.
