# Release notes: v2.1.0

Version 2.1.0 is a publication-hardening release. It does not change the public
Lean theorem statements or the pinned upstream proof revision.

## Highlights

- Clear public identity: **Lean Rooted-Tree Polymer Expansion**.
- Recommended repository slug: `lean-rooted-tree-polymer-expansion`.
- Committed and release-verified `lake-manifest.json`.
- Deterministic verification that consumes, rather than silently refreshes,
  dependency locks.
- Sectional and generated one-page article views from one Markdown source tree.
- Expanded formalization, notation, claims, release, and evaluator pages.
- New project identity, paper manifest, Lake pin, oracle log, and byte-for-byte
  release determinism checks.
- SPDX 2.3 JSON SBOM with a SHA-256 sidecar.
- Print-friendly browser rendering without a separately maintained PDF.

## Release contents

- complete article under `docs/paper/`;
- three stable Lean publication endpoints;
- exact upstream, Lean, Mathlib, and Lake dependency pins;
- strict documentation build and GitHub Pages workflow;
- theorem map, source provenance, oracle, evaluator guide, and reviewer FAQ;
- deterministic source ZIP, checksum, SBOM, and provenance workflow;
- governance, security, citation, archive, and migration metadata.

## Mathematical scope

The release formalizes finite rooted-tree and target-sensitive second-Ursell
bounds. It does not prove the model-specific raw Yang--Mills activity estimate,
`hRpoly`, a continuum construction, reconstruction, or a mass gap theorem.
