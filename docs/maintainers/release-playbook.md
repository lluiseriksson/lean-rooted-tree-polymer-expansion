# Release playbook

This page is the authoritative sequence for publishing a verified release.

## 1. Start from a clean checkout

```bash
git status --short
make docs-setup
make verify-nonlean
```

The local preflight intentionally avoids a potentially expensive kernel rebuild.
Do not tag a release if `lake-manifest.json`, the theorem manifest, generated
metadata, or the source manifest changes unexpectedly during verification.

A maintainer who explicitly wants additional local Lean evidence should use
`make lean`, never a raw `lake` command behind an external timeout. The
supervised target cleans up the entire process tree on timeout or interruption.
The required publication gate remains the green GitHub Actions Lean job.

## 2. Review the mathematical interface

- Confirm the three public theorem names and complete signatures.
- Confirm the theorem manifest and proof DAG still identify the exact pinned
  upstream sources.
- Inspect the GitHub Actions oracle output after the single CI kernel build.
- Confirm that no theorem claim has expanded beyond the source proof.
- Re-read the claims boundary and limitations pages.

## 3. Set and audit the release version

Use the structured updater rather than global search-and-replace:

```bash
python3 scripts/bump_version.py 2.4.2 --date 2026-06-23
```

Then write the changelog entry, refresh the reviewed source inventory, and run:

```bash
make manifest
make static
```

Check the version and date in `project.json`, `CITATION.cff`, CodeMeta, Zenodo
metadata, submission metadata, changelog, and release notes. Do not insert a DOI
before the archive has minted it.

## 4. Build deterministic release evidence

```bash
make package-determinism
```

This produces a source ZIP, per-file and aggregate checksums, SPDX 2.3 and
CycloneDX 1.5 SBOMs, deterministic build information, a deterministic in-toto
declaration, and a machine-readable release index in `release/`. It also
extracts the ZIP into a temporary clean-room tree and reruns the dependency-free
audits under the process-tree supervisor.

The deterministic in-toto statement is not an execution attestation. Confirm it
records `executionBound: false`; the tagged GitHub workflow supplies separate
hosted provenance attestations.

## 5. Push and wait for CI

Push the release commit without a tag. The pinned Lean action must show one
explicit `MarkedRootedClosure` build, the pinned environment checker, and then
`make lean-oracle`; a second full Lean build is a workflow-policy failure. Wait
for Lean verification, documentation, deterministic packaging, clean-room
archive checks, and Pages deployment. Record the final commit and workflow
URLs.

## 6. Tag and publish

Create a signed or annotated tag only after the clean CI run:

```bash
git tag -s v2.4.2 -m "v2.4.2 supervised verification and CI gate release"
git push origin v2.4.2
```

The release workflow verifies tag/version agreement, performs one Lean build,
audits the exact oracle, rebuilds deterministic evidence, requests hosted
provenance attestations, and publishes the ZIP, sidecars, both SBOMs, build info,
local in-toto declaration, release index, and aggregate checksums.

## 7. Archive and cite

After Zenodo or another archive has minted a DOI, add that DOI in a follow-up
metadata-only release. Preserve the exact versioned source archive and upstream
commit in the citation record.
