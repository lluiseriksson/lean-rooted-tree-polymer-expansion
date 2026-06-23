# Release notes: v2.4.0

Version 2.4.0 is a dependency-consistency, proof-traceability, accessibility,
and release-provenance hardening release. It preserves the exact three public
Lean theorem statements, upstream proof commit, Lean toolchain, Mathlib commit,
and mathematical claims boundary.

## Critical repair

The previous documentation environment simultaneously requested
`cffconvert==2.0.0` and `jsonschema==4.26.0`, although that CFF tool requires an
older incompatible JSON Schema line. This release removes the conflicting tool,
validates `CITATION.cff` against a committed project CFF profile, and uses one
modern JSON Schema implementation throughout. The unnecessary MkDocs minifier
chain has also been removed.

## Added

- `requirements-docs.lock`, a fully resolved exact transitive Python lock used
  by local setup, Docker, the dev container, and every documentation workflow;
- direct/transitive dependency-scope records in both SPDX 2.3 and CycloneDX 1.5
  SBOMs;
- `archive/proof-dag.json` and a rendered proof dependency graph linking the
  three public wrappers to their pinned upstream producers;
- version-consistency, Python-lock, proof-DAG, accessibility, syntax, archive
  extraction, metadata-profile, and provenance regression tests;
- deterministic in-toto Statement v1 / SLSA provenance, checksum sidecar, and
  release-index entry;
- a bounded safe ZIP extractor used by the clean-room smoke test.

## Release verification

The verifier now checks archive safety and completeness, archive-local manifest
digests, theorem and dependency pins, all locked Python packages in both SBOMs,
SBOM direct/transitive scope, build-info schema v2, release-index schema v2,
provenance subjects and resolved dependencies, aggregate checksums, and source
evidence digests. The full evidence set is built twice and must be byte-for-byte
identical.

## Release contents

- complete integrated article under `docs/paper/`;
- three stable Lean publication endpoints and exact axiom oracle;
- theorem manifest, proof DAG, source excerpts, statement fingerprints, and
  exact upstream Git blob IDs;
- exact Lean, Mathlib, elan-installer, GitHub Actions, and Python dependency
  pins;
- deterministic source ZIP, per-file sidecars, aggregate checksums;
- SPDX 2.3 and CycloneDX 1.5 SBOMs;
- build information, in-toto/SLSA provenance, and machine-readable release
  evidence index;
- strict MkDocs/Pages documentation with accessibility and internal-link
  audits.

## Mathematical scope

The release formalizes finite rooted-tree and target-sensitive second-Ursell
bounds. It does not prove the model-specific raw Yang--Mills activity estimate,
`hRpoly`, a continuum construction, Osterwalder--Schrader reconstruction, or a
mass gap theorem.
