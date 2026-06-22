# Submission checklist

The author or publishing agent should complete every item before submission.

## Repository and verification

- [ ] Replace the current repository tree using the v2.0.0 ZIP and remove legacy
      `paper/` and `release-artifacts/` directories.
- [ ] Run a fresh Lean build from an empty Lake cache.
- [ ] Record the green CI URL and final commit hash.
- [ ] Confirm the pinned upstream commit remains publicly accessible.
- [ ] Build the documentation with `mkdocs build --strict`.
- [ ] Enable GitHub Pages with **GitHub Actions** as the source.
- [ ] Review the deployed article on desktop and mobile.
- [ ] Create a signed or annotated `v2.0.0` tag and deterministic release ZIP.
- [ ] Archive that release on Zenodo or an institutional service.

## Scholarly metadata

- [ ] Confirm author affiliation, email, and ORCID outside the repository if the
      chosen venue requires them.
- [ ] Add the archive DOI to `CITATION.cff`, `codemeta.json`, and `.zenodo.json`.
- [ ] Run a fresh literature search for overlapping formalizations.
- [ ] Proofread every use of “first”, “new”, and “formalized”.
- [ ] Confirm the limitations paragraph remains prominent in the abstract,
      paper, README, and release notes.
- [ ] Confirm the target venue accepts a living HTML article or render the docs
      to its required format from the same Markdown sources.

## Release gate

Publication is blocked until `make verify` passes in CI. Local static checks do
not substitute for a Lean kernel rebuild.
