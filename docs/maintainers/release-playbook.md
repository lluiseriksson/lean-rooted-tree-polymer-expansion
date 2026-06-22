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

## 3. Audit publication metadata

```bash
make static
```

Check the version and date in `project.json`, `CITATION.cff`, CodeMeta, Zenodo
metadata, submission metadata, changelog, and release notes. Do not insert a DOI
before the archive has minted it.

## 4. Build the deterministic artifact

```bash
make package
```

This produces a source ZIP, SHA-256 sidecar, and SPDX 2.3 JSON SBOM in
`release/`. The release script runs twice in CI and requires byte-for-byte
identical archives.

## 5. Push and wait for CI

Push the release commit without a tag. Wait for both the Lean verification and
documentation workflows to complete successfully. Inspect the Pages deployment.

## 6. Tag and publish

Create a signed or annotated tag only after the clean CI run:

```bash
git tag -s v2.1.0 -m "v2.1.0 publication-hardening release"
git push origin v2.1.0
```

The release workflow rebuilds the artifact, attests provenance, and publishes
the ZIP, checksum, and SBOM.

## 7. Archive and cite

After Zenodo or another archive has minted a DOI, add that DOI in a follow-up
metadata-only release. Preserve the exact versioned source archive and upstream
commit in the citation record.
