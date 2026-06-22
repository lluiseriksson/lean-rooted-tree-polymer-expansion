# Changelog

All notable changes to this publication artifact are recorded here.

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
