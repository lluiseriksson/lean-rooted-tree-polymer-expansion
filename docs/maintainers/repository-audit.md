# Repository audit and migration decision

**Audit date:** 2026-06-22  
**Remote:** `lluiseriksson/marked-rooted-closure`

## Verification of the existing repository

The remote README was inspected through the GitHub connector and matches the
v1.0.0 delivery at the level of repository structure and publication content.
It identifies the repository as a bundle containing:

- the manuscript and graphical abstract;
- the Lean 4 companion and its three public theorem endpoints;
- the exact upstream source lock;
- CI and artifact checks;
- citation and submission metadata;
- reviewer and publishing-agent documentation;
- preserved copies of the originally supplied release artifacts.

The three endpoint names shown remotely are the same ones in the supplied
v1.0.0 archive:

```text
MarkedRootedClosure.normalizedRootedChildFactorialTreeBound
MarkedRootedClosure.markedRootLeafGeometricBound
MarkedRootedClosure.targetPreservingWeightedTreeBound
```

This is a **structural/content audit**, not a byte-for-byte cryptographic audit
of every remote binary. The original local v1.0.0 ZIP and its SHA-256 sidecar
remain the authoritative byte-level record of the delivery.

## Why the remote still needs replacement

The remote is organized around a separately tracked manuscript binary and a
second LaTeX manuscript source. It also preserves nested copies of previous
release artifacts. That arrangement conflicts with the current requirement:
the article must live in the repository documentation and must not be uploaded
as an independent paper file.

## Decision for v2.0.0

Version 2.0.0 therefore:

- preserves the three Lean theorem claims and wrapper interface;
- updates the immutable upstream pin to the current verified theorem-bearing
  commit;
- migrates the complete article to `docs/paper/`;
- adds a strict MkDocs build and GitHub Pages deployment;
- removes standalone manuscript binaries and duplicated LaTeX sources;
- removes nested copies of old ZIP and manuscript artifacts;
- adds delete-aware migration instructions;
- expands CI, release, security, governance, metadata, and link checks;
- produces a deterministic source-only archive with a SHA-256 sidecar.

The v2 tree must replace the repository with deletion enabled. Copying it as a
simple overlay would leave the legacy publication model in place.
