# Upload and migration instructions

Version 2.1.0 should replace the working tree, not be copied as a partial
overlay.

## Safe procedure

```bash
git clone https://github.com/lluiseriksson/lean-rooted-tree-polymer-expansion.git
cd marked-rooted-closure
rsync -a --delete --exclude='.git/' \
  /path/to/lean-rooted-tree-polymer-expansion-v2.1.0/ ./
make static

git status --short
git add -A
git commit -m "release: harden integrated publication artifact v2.1.0"
git push origin main
```

The release ZIP contains `lake-manifest.json`; verify that it remains tracked.
Ordinary builds must not rewrite it.

## After the push

1. Wait for the `verify` and `documentation` workflows.
2. Set Pages deployment to **GitHub Actions** if it is not already enabled.
3. Protect `main` and require the Lean and documentation checks.
4. Inspect the deployed site, including formulas, search, edit links, and the
   generated continuous article.
5. Create tag `v2.1.0` only after all checks pass.
6. Confirm that the release includes the ZIP, SHA-256 sidecar, SPDX SBOM, and
   provenance attestation.
7. Archive the verified release and update DOI metadata in a later commit.

## Optional rename

Once the release is stable, the repository may be renamed to
`lean-rooted-tree-polymer-expansion`. Use the
[rename proposal and checklist](rename-repository.md); do not manually edit a
subset of URLs.
