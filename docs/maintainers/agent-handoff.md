# Publishing-agent handoff

## Mission

Install the v2.4.0 tree, run the complete verification workflow, deploy the
integrated article through GitHub Pages, and publish an immutable source release
without broadening the mathematical claims.

## Safe installation

From a clean clone:

```bash
rsync -a --delete --exclude='.git/' \
  /path/to/lean-rooted-tree-polymer-expansion-v2.4.0/ ./
make test
make static
git status --short
```

The delete-aware copy prevents obsolete rename-proposal files, standalone paper
artifacts, or nested historical releases from surviving.

## Verification gate

A release is blocked until all of the following hold:

1. `make test`, `make static`, and `make docs` succeed;
2. the clean-cache Lean CI job succeeds;
3. the oracle output contains no `sorryAx` or project-local axiom;
4. the deployed Pages site has been checked on desktop and mobile;
5. deterministic packaging succeeds twice byte for byte;
6. the source ZIP passes the clean-room smoke test;
7. ZIP, sidecars, SPDX SBOM, CycloneDX SBOM, build information, release index,
   and aggregate checksums verify as one set;
8. the final commit and workflow URLs are recorded;
9. any DOI is added only after it is minted.

## Claims discipline

The result is finite and orderwise. Do not advertise it as a proof of
`hRpoly`, a raw Yang--Mills activity estimate, a continuum construction, or a
mass gap. Do not turn qualified novelty language into an unconditional priority
claim without a fresh literature review.

## Release-critical files

- `project.json` and `schemas/project.schema.json`
- `lakefile.lean`, `lake-manifest.json`, and `lean-toolchain`
- `archive/UPSTREAM.lock`, `archive/theorem-manifest.json`, and
  `archive/actions-manifest.json`
- `MarkedRootedClosure/PaperTheorems.lean` and `MarkedRootedClosure/Oracle.lean`
- `docs/paper/manifest.json` and `docs/llms.txt`
- `docs/artifact/verification-contract.md`
- `scripts/check_theorem_manifest.py`, `scripts/check_oracle_output.py`, and
  `scripts/check_workflows.py`
- `scripts/verify_release.py`
- the claims-boundary language throughout the site
