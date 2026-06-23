# Build status and verification boundary

**Package assembly date:** 2026-06-23

## Locally audited for this source package

- 31 dependency-free regression tests for repository tooling;
- repository structure and required-file inventory;
- project schema, identity, URL, date, and version consistency;
- upstream, Mathlib, Lean, Lake-manifest, elan-installer, and source-blob pin
  consistency;
- public theorem names, normalized statement fingerprints, offline excerpts,
  exact source blobs, article pages, theorem map, and negative claims;
- exact oracle-log parser behavior, including rejection of extra axioms;
- paper section manifest and generated continuous article;
- bibliography keys and rendered DOI/arXiv/repository identifiers;
- internal Markdown links and anchors;
- external GitHub Action inventory, workflow permissions, canonical-repository
  guards, release outputs, and cold-cache maintenance policy;
- machine-readable agent index;
- absence of `sorry`, `admit`, tracked standalone PDFs, and legacy release
  directories;
- deterministic source archive generation and archive-local manifest;
- ZIP traversal, duplicate-name, case-folding, Unicode-normalization, symlink,
  encryption, non-regular-entry, malformed-manifest, and size-limit defenses;
- SPDX 2.3 and CycloneDX 1.5 SBOM structure;
- deterministic build-information and release-index hashes;
- aggregate release checksums;
- clean-room extraction followed by source-tree audits.

## CI-required gates

A source-package assembly environment does not by itself certify a fresh Lean
kernel rebuild or the deployed Pages site. Before tagging v2.4.0, the uploaded
repository workflows must confirm:

- fresh Lean kernel compilation from the committed Lake graph;
- exact axiom-oracle output for all three endpoints;
- strict MkDocs Material build;
- GitHub Pages deployment and visual inspection;
- deterministic package and clean-room jobs;
- release-index and checksum verification;
- provenance attestations for the tagged release evidence.

A publishing agent must not describe those gates as complete until the
corresponding workflow URLs are green.
