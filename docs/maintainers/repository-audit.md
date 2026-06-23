# Repository audit for v2.4.0

**Audit date:** 2026-06-23
**Current remote:** `lluiseriksson/lean-rooted-tree-polymer-expansion`
**Audited live base:** `v2.1.0` at commit
`5ae9e7670e9bd53be0517741d00c91ecea2b3046`

## Base state confirmed

The public repository already exposed the integrated article, three stable Lean
theorem aliases, exact source locks, CI, GitHub Pages deployment, evaluator
material, and deterministic release tooling. The adopted repository name and
stable Lean namespace were already consistent in the live v2.1.0 tree.

## Improvements accumulated in v2.2.0

- Added executable JSON schemas for project and theorem-manifest metadata.
- Added cross-checks from theorem records to Lean declarations, upstream names,
  article pages, theorem maps, locks, and negative claims.
- Added dependency-free tooling tests, workflow-policy checks, CycloneDX, build
  information, deterministic evidence checks, and clean-room ZIP auditing.
- Removed obsolete rename-proposal material while preserving an explicit
  repository-history record.

## Additional hardening in v2.4.0

1. **Statement-level proof identity.** Each public theorem declaration now has a
   whitespace-stable SHA-256 fingerprint, so binder or conclusion drift is
   detected even when a theorem name remains unchanged.
2. **Pinned source objects.** The two upstream Lean files containing the proofs
   are recorded by exact Git blob object ID as well as repository commit.
3. **Exact axiom contract.** The oracle parser now requires exactly
   `[propext, Classical.choice, Quot.sound]` for each public endpoint; extra,
   missing, or malformed reports fail.
4. **Reference integrity.** BibTeX keys and rendered DOI/arXiv/repository links
   are checked as one scholarly bibliography.
5. **Workflow inventory.** Every external GitHub Action is pinned by full
   immutable commit SHA in a machine-readable manifest; unlisted, mutable, or
   policy-breaking uses fail.
6. **Cold-cache maintenance.** A scheduled workflow rebuilds Lean without the
   GitHub Lean cache and reruns documentation, deterministic packaging, and the
   clean-room archive test.
7. **Pinned bootstrap.** The Docker elan installer is fetched from an exact
   commit and verified against its Git blob object ID before execution.
8. **Release evidence graph.** A machine-readable release index and aggregate
   checksums bind the ZIP, SPDX SBOM, CycloneDX SBOM, build information, proof
   pins, and source manifest.
9. **Archive attack resistance.** Verification rejects duplicate names,
   path traversal, case-folding and Unicode-normalization collisions, symlinks,
   non-regular members, encryption, malformed manifests, and size abuse.
10. **Agent-safe discovery.** `docs/llms.txt` gives tools a compact canonical
    map of theorem endpoints, proof pins, high-value files, and claim limits.
11. **Expanded regression suite.** Tooling tests cover signature stability,
    exact oracle parsing, references, workflow drift, agent indexing, and
    malicious ZIP constructions.

## Preserved mathematical interface

```text
MarkedRootedClosure.normalizedRootedChildFactorialTreeBound
MarkedRootedClosure.markedRootLeafGeometricBound
MarkedRootedClosure.targetPreservingWeightedTreeBound
```

No theorem statement, upstream proof commit, Lean toolchain, Mathlib revision,
or mathematical claim changes in this release.

## External release gate

The assembled source package can run all dependency-free audits and release
integrity checks locally. A fresh Lean kernel rebuild, exact oracle run, strict
MkDocs build, Pages inspection, and tagged provenance attestation remain
mandatory GitHub Actions gates before publishing v2.4.0.

## v2.4.0 audit delta

The audit found and removed a real dependency conflict between the former CFF
validator and the pinned modern JSON Schema package. The replacement uses a
committed CFF profile, a complete exact transitive Python lock, dual-SBOM lock
coverage, proof-DAG checks, accessibility checks, safe archive extraction, and
deterministic in-toto/SLSA provenance. Public Lean statements and proof pins are
unchanged.
