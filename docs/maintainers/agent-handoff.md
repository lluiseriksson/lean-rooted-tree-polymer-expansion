# Publishing-agent handoff

## Mission

Install the v2.4.2 tree, run the complete non-Lean source-package verification,
let GitHub Actions perform the authoritative single Lean build and exact oracle,
deploy the integrated article, and publish an immutable source release without
broadening the mathematical claims.

## Safe installation

From a clean clone:

```bash
rsync -a --delete --exclude='.git/' \
  /path/to/lean-rooted-tree-polymer-expansion-v2.4.2/ ./
make docs-setup
make verify-nonlean
make package-determinism
git status --short
```

The delete-aware copy prevents obsolete rename-proposal files, standalone paper
artifacts, nested historical releases, or stale helper scripts from surviving.

## Lean execution policy

The publication gate is GitHub Actions on the pinned Linux environment. The
pinned Lean action must build `MarkedRootedClosure` once with automatic feature
detection disabled and `leanchecker: true`; the next step runs only
`make lean-oracle`.

A local Lean run is optional supporting evidence. Use `make lean`,
`make lean-build`, or `make lean-oracle`. Those targets isolate the command in a
process group and terminate every descendant on timeout, interrupt, or parent
loss. Do not launch a raw long-running `lake` command through an external timeout
and do not kill unrelated Lean processes on the host.

## Verification gate

A release is blocked until all of the following hold:

1. `make verify-nonlean` succeeds;
2. deterministic packaging succeeds twice byte for byte;
3. the source ZIP passes the supervised clean-room smoke test;
4. the GitHub Actions single-build Lean job succeeds;
5. the oracle output contains exactly the documented three axioms and no
   `sorryAx` or project-local axiom;
6. the deployed Pages site has been checked on desktop and mobile;
7. ZIP, sidecars, SPDX SBOM, CycloneDX SBOM, build information, deterministic
   in-toto declaration, release index, and aggregate checksums verify as one set;
8. the deterministic in-toto metadata says `executionBound: false` and the
   tagged artifacts have separate hosted GitHub attestations;
9. the final commit and workflow URLs are recorded;
10. any DOI is added only after it is minted.

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
- `MANIFEST.sha256`, `scripts/source_inventory.py`, and
  `scripts/check_source_manifest.py`
- `scripts/process_runner.py` and `scripts/run_lean_gate.py`
- `scripts/check_theorem_manifest.py`, `scripts/check_oracle_output.py`, and
  `scripts/check_workflows.py`
- `scripts/generate_provenance.py` and `scripts/verify_release.py`
- the claims-boundary language throughout the site
