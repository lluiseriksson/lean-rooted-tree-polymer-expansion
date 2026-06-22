# Upload and migration instructions

The GitHub repository already contains the earlier v1 bundle. This package is a
replacement tree, not an additive overlay.

## Safe procedure

```bash
git clone https://github.com/lluiseriksson/marked-rooted-closure.git
cd marked-rooted-closure
rsync -a --delete --exclude='.git/' \
  /path/to/marked-rooted-closure-v2.0.0/ ./
make static

git status --short
git add -A
git commit -m "release: documentation-integrated v2.0.0 artifact"
git push origin main
```

`rsync --delete` is required so the old standalone `paper/` directory and
nested `release-artifacts/` are removed.

## After the push

1. Wait for the `verify` and `documentation` workflows to finish.
2. In repository settings, select **GitHub Actions** as the Pages source.
3. Protect `main` and require the Lean and docs checks.
4. Create tag `v2.0.0` only after all checks pass.
5. Run the release workflow or `make release` and attach the resulting ZIP and
   SHA-256 sidecar.
6. Archive the release and update DOI metadata in a follow-up commit.
