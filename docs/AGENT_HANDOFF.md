# Publishing-agent handoff

## Mission

Publish this frozen artifact as a new repository and submit the manuscript
without broadening its mathematical claims.

Suggested repository name:

```text
marked-rooted-closure
```

Suggested release tag:

```text
v1.0.0
```

## Non-negotiable claims discipline

The headline result is finite and orderwise. Do not advertise it as a proof of
the Yang-Mills mass gap, `hRpoly`, a continuum limit, or a new theory of
cardinal infinity. Do not replace the phrase “to the best of our knowledge” by
an unconditional novelty claim.

## Publication gate

Do not submit until all of the following are green:

1. A clean GitHub Actions Lean build from an empty cache.
2. `lake env lean MarkedRootedClosure/Oracle.lean` shows only the expected
   standard classical axioms.
3. `make -C paper clean all` rebuilds `paper/main.pdf`.
4. Every PDF page has been visually inspected.
5. The final release ZIP hash has been recorded.
6. The repository URL and archived DOI have been inserted into metadata.
7. Author email, affiliation, and ORCID have been confirmed.
8. A fresh literature search has been completed.

## Recommended release sequence

1. Create a new public repository from this ZIP.
2. Preserve `archive/UPSTREAM.lock`, `lean-toolchain`, and the exact SHA in
   `lakefile.lean`.
3. Push and run CI from a clean cache.
4. Add the final repository URL to `CITATION.cff`, `codemeta.json`, and the
   manuscript artifact paragraph.
5. Create release `v1.0.0`; attach the clean source ZIP, SHA-256 file, paper PDF,
   and graphical abstract.
6. Archive the release on Zenodo or an institutional service.
7. Add the DOI to `CITATION.cff` and `.zenodo.json`.
8. Submit the paper with the immutable release URL.

## Editorial positioning

Use `docs/EDITORIAL_POSITIONING.md`. The natural audiences are formalized
mathematics / theorem proving and rigorous mathematical physics. Venue choice
must be based on current calls, policies, and page limits; acceptance cannot be
guaranteed.

## Files to edit before submission

- `paper/main.tex`: affiliation, email, ORCID, final artifact URL, archive DOI.
- `paper/cover-letter.md`: editor and venue.
- `CITATION.cff`: final repository URL and DOI.
- `codemeta.json`: final repository URL and DOI.
- `.zenodo.json`: archive metadata.
- `paper/author-declarations.md`: funding and policy-specific declarations.

## Files not to loosen

- `archive/UPSTREAM.lock`
- `archive/theorem-manifest.json`
- `lean-toolchain`
- the exact upstream SHA in `lakefile.lean`
- the scope and limitations language
- the three publication-facing theorem statements
