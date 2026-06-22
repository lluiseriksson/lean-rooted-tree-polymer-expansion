# Submission checklist

## Repository and verification

- [ ] Install the complete v2.1.0 replacement tree with deletion enabled.
- [ ] Confirm `lake-manifest.json` is tracked and unchanged by ordinary builds.
- [ ] Run a fresh Lean build from an empty Lake cache.
- [ ] Inspect the oracle output and record the green CI URL and final commit.
- [ ] Build MkDocs in strict mode and inspect both sectional and continuous
      article views on desktop and mobile.
- [ ] Confirm GitHub Pages uses the Actions deployment workflow.
- [ ] Protect `main` and require Lean and documentation checks.
- [ ] Run deterministic packaging and verify the ZIP, checksum, SPDX SBOM, and
      provenance attestation.
- [ ] Create a signed or annotated `v2.1.0` tag only after all gates pass.
- [ ] Archive the exact tagged release.

## Scholarly metadata

- [ ] Confirm author affiliation, email, and ORCID if required by the venue.
- [ ] Add an archive DOI only after it has been minted, then update CFF,
      CodeMeta, Zenodo metadata, and the article consistently.
- [ ] Run a fresh literature search for overlapping mathematical and Lean
      formalizations.
- [ ] Proofread every use of “first”, “new”, “formalized”, and “verified”.
- [ ] Confirm the limitations paragraph remains prominent in the abstract,
      README, article, release notes, and archive description.
- [ ] Confirm the venue accepts a living HTML article or generate its required
      submission format from the same Markdown sources without creating a
      second maintained manuscript.

## Optional rename

- [ ] Decide whether to adopt `lean-rooted-tree-polymer-expansion`.
- [ ] Rename the GitHub repository before running the metadata migration script.
- [ ] Verify the new Pages URL, badges, issue links, citation URLs, release
      prefix, and archive integrations.

Publication is blocked until the Lean and documentation workflows are green.
Local static checks do not substitute for a kernel rebuild.
