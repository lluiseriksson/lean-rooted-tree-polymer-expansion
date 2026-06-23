# Changelog

All notable changes to this publication artifact are recorded here.

## 2.4.0 - 2026-06-23

### Fixed

- Replaced an internally inconsistent documentation dependency set: the former
  CFF validator required `jsonschema<4` while the repository pinned
  `jsonschema==4.26.0`. Metadata validation now uses a committed local CFF
  profile and the same modern JSON Schema engine as the rest of the artifact.
- Removed the unnecessary documentation minifier dependency chain, eliminating
  source-only transitive packages from clean environment installation.
- Replaced `ZipFile.extractall` in the clean-room smoke test with a validated,
  bounded, path-safe extractor.

### Added

- A fully resolved `requirements-docs.lock` and audits enforcing exact direct
  and transitive Python pins.
- A machine-readable proof dependency DAG linking the three public Lean
  endpoints to their pinned upstream producers.
- Version-consistency, accessibility, syntax, Python-lock, proof-DAG, and
  provenance checks, with focused regression tests.
- Deterministic in-toto Statement v1 / SLSA provenance and its checksum as
  first-class release evidence.
- Machine-readable schemas for the CFF profile, proof DAG, and provenance
  statement, plus a safe release-extraction library.

### Changed

- SBOM generation now enumerates the complete transitive Python lock and marks
  the four direct documentation dependencies explicitly.
- Build information and the release index use schema version 2 and include the
  Python lock, proof DAG, CFF profile, and in-toto provenance.
- GitHub Actions, Docker, the dev container, and local bootstrap commands all
  install the same committed transitive lock.
- Release verification now checks provenance subjects, resolved dependency
  digests, expanded source evidence, aggregate checksums, and safe extraction.
- The integrated documentation explains the proof graph, dependency lock, and
  complete release-evidence chain.

## 2.3.0 - 2026-06-23

### Preserved

- The three public Lean theorem statements and the exact upstream proof, Lean,
  and Mathlib revisions.
- The integrated-documentation model, stable `MarkedRootedClosure` API, and
  explicit negative claims boundary.
- The source-only release policy with no separately maintained manuscript PDF.

### Improved

- Added whitespace-stable SHA-256 fingerprints for every public Lean theorem
  statement and Git blob IDs for the two pinned upstream proof files.
- Strengthened the oracle audit from a forbidden-token check to exact equality
  with `[propext, Classical.choice, Quot.sound]` for every endpoint.
- Added a scholarly reference audit linking canonical BibTeX entries to rendered
  DOI, arXiv, and repository identifiers.
- Pinned every external GitHub Action to a full immutable commit SHA, added a
  machine-readable action manifest, canonical-repository guards, and monthly
  cold-cache verification.
- Pinned the Docker elan installer script by commit and Git blob object ID.
- Added a release evidence index and aggregate checksum file binding the source
  ZIP, SPDX SBOM, CycloneDX SBOM, and deterministic build information.
- Hardened ZIP verification against duplicate names, case-folding and Unicode
  collisions, non-regular entries, malformed manifest rows, and archive size
  abuse.
- Added JSON schemas for paper, build-information, action, and release-index
  metadata.
- Added an agent-readable `llms.txt`, repository-settings guide, and expanded
  dependency-free tests for signatures, axioms, workflows, references, and
  malicious archives.

## 2.2.0 - 2026-06-22

### Preserved

- The three public Lean theorem statements and the pinned upstream proof revision.
- The integrated-documentation publication model and explicit claims boundary.
- The stable `MarkedRootedClosure` Lean package and namespace.

### Improved

- Recorded the adopted `lean-rooted-tree-polymer-expansion` identity and removed
  obsolete rename-proposal pages.
- Added JSON schemas for project and theorem-manifest metadata.
- Added cross-checks from the theorem manifest to Lean declarations, upstream
  names, article pages, theorem maps, locks, and negative claims.
- Added a dependency-free unit-test suite for repository tooling.
- Added a GitHub Actions workflow security and release-output audit.
- Added CycloneDX 1.5 alongside the SPDX 2.3 SBOM.
- Added deterministic build information binding the ZIP and both SBOMs.
- Hardened ZIP verification against traversal, symlinks, encryption, unlisted
  files, proof-pin drift, and evidence mismatch.
- Added a clean-room source-archive smoke test.
- Added verification-contract, release-evidence, citation, and repository-history
  documentation.

## 2.1.0 - 2026-06-22

### Preserved

- The three public Lean theorem statements and their upstream proof revision.
- The integrated-documentation publication model and explicit claims boundary.

### Improved

- Added the authoritative `lake-manifest.json` to the distributable source tree.
- Removed `lake update` from ordinary verification; dependency refresh is now
  an explicit maintenance target.
- Rebranded the documentation site as **Lean Rooted-Tree Polymer Expansion**
  while keeping the stable Lean namespace.
- Added a migration-safe proposal to rename the repository to
  `lean-rooted-tree-polymer-expansion`.
- Added project-identity, Lake-lock, paper-manifest, oracle-log, and release
  determinism audits.
- Added a generated continuous article derived from the same canonical Markdown
  sections, plus browser-print styling.
- Added an SPDX 2.3 JSON SBOM and checksum to release packaging.
- Reworked the landing page, formalization map, claims page, notation guide,
  release playbook, agent handoff, and submission checklist.
- Updated static checks so the release ZIP cannot omit the dependency manifest.

## 2.0.0 - 2026-06-22

### Changed

- Integrated the complete article into the MkDocs documentation tree.
- Removed tracked standalone paper PDFs, duplicated LaTeX sources, and nested
  historical release artifacts.
- Updated the immutable upstream proof pin to
  `4e45246aa109671d25fcd01ba1abf7bc3f8506d1`.
- Reworked README, citation metadata, Zenodo metadata, and release tooling for a
  documentation-first publication model.

### Added

- Strict MkDocs Material build with MathJax and GitHub Pages deployment.
- Expanded theorem map, provenance, evaluator guide, reviewer FAQ, and
  publishing-agent migration instructions.
- Internal-link, lock-consistency, metadata, stale-path, and release audits.
- Security policy, contribution policy, issue forms, pull-request template,
  CODEOWNERS, and dependency-update configuration.
- Deterministic source-only release archive and manifest generation.

## 1.0.0 - 2026-06-22

- Initial PDF-based publication bundle.
- Added three stable Lean theorem aliases.
- Added pinned upstream, toolchain, and Mathlib metadata.
- Added CI, oracle, artifact checks, and submission handoff.
