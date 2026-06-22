# Publishing-agent handoff

## Mission

Replace the repository contents with the v2.1.0 tree, run the complete
verification workflow, deploy the integrated article through GitHub Pages, and
publish an immutable source release without broadening the mathematical claims.

## Safe installation

From a clean clone of the current repository:

```bash
rsync -a --delete --exclude='.git/' \
  /path/to/lean-rooted-tree-polymer-expansion-v2.1.0/ ./
make static
git status --short
```

Then commit and push the complete replacement. The delete-aware copy prevents
legacy standalone paper or nested release artifacts from reappearing.

## Verification gate

A release is blocked until all of the following hold:

1. `make static` succeeds.
2. `make docs` succeeds in strict mode.
3. the clean-cache Lean CI job succeeds;
4. the oracle output contains no `sorryAx` or project-local axiom;
5. the deployed Pages site has been checked on desktop and mobile;
6. the deterministic ZIP, checksum, and SPDX SBOM have been verified;
7. the final commit and workflow URLs have been recorded;
8. any DOI has been added only after it is minted.

## Claims discipline

The result is finite and orderwise. Do not advertise it as a proof of
`hRpoly`, a raw Yang--Mills activity estimate, a continuum construction, or a
mass gap. Do not turn qualified novelty language into an unconditional priority
claim without a fresh literature review.

## Optional repository rename

The recommended slug is `lean-rooted-tree-polymer-expansion`. Apply the rename
only after the v2.1.0 tree is green under the current name. Follow
[the dedicated rename checklist](rename-repository.md), then run the included
metadata migration script. The Lean namespace remains unchanged.

## Release-critical files

- `project.json`
- `lakefile.lean`
- `lake-manifest.json`
- `lean-toolchain`
- `archive/UPSTREAM.lock`
- `archive/theorem-manifest.json`
- `MarkedRootedClosure/PaperTheorems.lean`
- `MarkedRootedClosure/Oracle.lean`
- `docs/paper/manifest.json`
- `docs/artifact/theorem-map.md`
- the claims-boundary language throughout the site
