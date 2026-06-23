# Release playbook

This page is the authoritative sequence for publishing a verified release.

## 1. Start from a clean checkout

```bash
git status --short
make docs-setup
make verify
```

Do not tag a release if `lake-manifest.json`, the theorem manifest, or generated
metadata changes unexpectedly during verification.

## 2. Review the mathematical interface

- Confirm the three public theorem names and complete signatures.
- Run the oracle and inspect its output.
- Confirm that no theorem claim has expanded beyond the source proof.
- Re-read the claims boundary and limitations pages.

## 3. Set and audit the release version

Use the structured updater rather than global search-and-replace:

```bash
python3 scripts/bump_version.py 2.4.0 2026-06-23
```

Then write the changelog entry and run:

```bash
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
CycloneDX 1.5 SBOMs, deterministic build information, and a machine-readable
release index in `release/`. It also extracts the ZIP into a temporary
clean-room tree and reruns the dependency-free audits.

## 5. Push and wait for CI

Push the release commit without a tag. Wait for Lean verification,
documentation, deterministic packaging, and clean-room archive checks. Inspect
the Pages deployment.

## 6. Tag and publish

Create a signed or annotated tag only after the clean CI run:

```bash
git tag -s v2.4.0 -m "v2.4.0 traceability and release-integrity release"
git push origin v2.4.0
```

The release workflow rebuilds the artifact, verifies tag/version agreement,
attests hosted provenance, and publishes the ZIP, sidecars, both SBOMs, build
info, local in-toto provenance, release index, and aggregate checksums.

## 7. Archive and cite

After Zenodo or another archive has minted a DOI, add that DOI in a follow-up
metadata-only release. Preserve the exact versioned source archive and upstream
commit in the citation record.
