# Submission checklist

## Repository and verification

- [ ] Install the complete v2.4.2 replacement tree with deletion enabled.
- [ ] Confirm `lake-manifest.json` is tracked and unchanged by ordinary builds.
- [ ] Run `make verify-nonlean` and `make package-determinism` locally.
- [ ] Confirm GitHub Actions performs one explicit Lean build from the committed Lake graph.
- [ ] Inspect the subsequent `make lean-oracle` output, confirm the exact
      three-axiom set for every endpoint, and record the green CI URL and final commit.
- [ ] Build MkDocs in strict mode and inspect sectional and continuous article
      views on desktop and mobile.
- [ ] Confirm GitHub Pages uses the Actions deployment workflow and that
      `docs/llms.txt` is reachable from the deployed site.
- [ ] Protect `main` and require Lean, documentation, and package checks.
- [ ] Verify deterministic ZIP generation and the clean-room archive smoke test.
- [ ] Verify ZIP and JSON sidecars, aggregate checksums, SPDX SBOM, CycloneDX
      SBOM, build info, release index, deterministic in-toto declaration, and
      separate hosted provenance attestations.
- [ ] Create a signed or annotated `v2.4.2` tag only after all gates pass.
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

Publication is blocked until the Lean, documentation, and release-evidence
workflows are green. Local static checks do not substitute for a kernel rebuild.
