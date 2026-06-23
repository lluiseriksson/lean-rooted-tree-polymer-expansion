# Build status and verification boundary

**Package assembly date:** 2026-06-23

## Locally audited for this source package

- dependency-free regression tests for repository tooling;
- repository structure and required-file inventory;
- project schema, identity, URL, date, and version consistency;
- upstream, Mathlib, Lean, Lake-manifest, elan-installer, and source-blob pin
  consistency;
- public theorem names, normalized statement fingerprints, offline excerpts,
  exact source blobs, article pages, theorem map, and negative claims;
- exact oracle-log parser behavior, including rejection of extra axioms;
- supervised process-group behavior for success, nonzero exit, timeout,
  descendant cleanup, and parent-process loss;
- fake-Lake regression coverage for exact oracle acceptance, lock drift, and
  retained failure logs;
- paper section manifest and generated continuous article;
- bibliography keys and rendered DOI/arXiv/repository identifiers;
- internal Markdown links and anchors;
- external GitHub Action inventory, workflow permissions, canonical-repository
  guards, release outputs, and cold-cache maintenance policy;
- machine-readable agent index;
- absence of `sorry`, `admit`, tracked standalone PDFs, and legacy release
  directories;
- committed source-manifest freshness, deterministic source archive generation,
  and archive-local manifest verification;
- ZIP traversal, duplicate-name, non-canonical-alias, file/directory,
  case-folding, Unicode-normalization, Windows-reserved-name, symlink, encryption,
  non-regular-entry, malformed-manifest, and size-limit defenses;
- SPDX 2.3 and CycloneDX 1.5 SBOM structure;
- deterministic build-information and release-index hashes;
- aggregate release checksums;
- clean-room extraction followed by source-tree audits;
- deterministic local provenance that explicitly declines to claim hosted
  execution and requires a separate GitHub attestation.

## CI-required gates

A source-package assembly environment does not by itself certify a fresh Lean
kernel rebuild or the deployed Pages site. Before tagging v2.4.2, the uploaded
repository workflows must confirm:

- one explicit Lean kernel compilation from the committed Lake graph;
- exact axiom-oracle output for all three endpoints after that build;
- strict MkDocs Material build;
- GitHub Pages deployment and visual inspection;
- deterministic package and clean-room jobs;
- release-index and checksum verification;
- provenance attestations for the tagged release evidence.

A publishing agent must not describe those gates as complete until the
corresponding workflow URLs are green.
