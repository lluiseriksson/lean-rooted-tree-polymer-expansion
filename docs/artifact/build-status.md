# Build status and verification boundary

**Package assembly date:** 2026-06-22

## Locally audited for this source package

- repository structure and required-file inventory;
- JSON and YAML syntax available in the assembly environment;
- project identity and URL consistency;
- upstream, Mathlib, Lean, and Lake-manifest pin consistency;
- paper section manifest and generated continuous article;
- internal Markdown link targets;
- absence of `sorry`, `admit`, tracked standalone PDFs, and legacy release
  directories;
- deterministic source archive generation, archive-local manifest, checksums,
  and SPDX SBOM structure;
- Python syntax and shell-script parse checks.

## CI-required gates

The package-assembly environment does not provide outbound Git, the pinned Lean
toolchain cache, or the MkDocs dependencies. Therefore the following must be
confirmed by the uploaded repository workflows before release:

- fresh Lean kernel compilation;
- axiom-oracle output;
- strict MkDocs Material build;
- GitHub Pages deployment;
- provenance attestation for the tagged source archive.

A publishing agent must not describe those gates as complete until the
corresponding workflow URLs are green.
