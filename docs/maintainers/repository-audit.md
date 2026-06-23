# Repository audit for v2.4.3

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

## Hardening accumulated through v2.4.1

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
9. **Archive attack resistance.** Verification rejects duplicate or
   non-canonical names, path traversal, file/directory conflicts, case-folding
   and Unicode-normalization collisions, Windows-reserved names, symlinks,
   non-regular members, encryption, malformed manifests, and size abuse.
10. **Agent-safe discovery.** `docs/llms.txt` gives tools a compact canonical
    map of theorem endpoints, proof pins, high-value files, and claim limits.
11. **Expanded regression suite.** Tooling tests cover signature stability,
    exact oracle parsing, references, workflow drift, agent indexing, and
    malicious ZIP constructions.

## Execution safety added in v2.4.2

- Replaced raw long-running local Lean/Lake calls with a dependency-free
  process-tree supervisor that handles timeout, interrupt, parent loss, and
  residual background descendants.
- Configured the pinned Lean action for one explicit `MarkedRootedClosure`
  build plus `leanchecker`, followed only by the exact-oracle audit.
- Required byte-identical `lake-manifest.json` across local build and oracle
  phases and kept failed oracle logs for diagnosis.
- Corrected deterministic provenance so it declares a reproducible recipe with
  `executionBound: false` while hosted attestations remain separate evidence.

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
integrity checks locally. The authoritative GitHub Actions gate performs one
explicit Lean kernel build from the committed Lake graph, runs the exact oracle,
builds strict documentation, deploys Pages, reproduces the package, smoke-tests
the archive, and transfers the exact candidate from a read-only job to a
separate tag-only publisher.

## v2.4.3 audit delta

The published v2.4.2 correction demonstrated that broad release globs can map
one file to multiple command arguments: the aggregate `.checksums.sha256` file
also matched the generic `*.sha256` pattern. The local release was valid, but
publication needed a manual workflow correction to avoid the duplicate asset.

v2.4.3 turns that incident into an enforced protocol. One shared module defines
six primary artifacts, their six sidecars, and one aggregate checksum. Every
sidecar and the aggregate are compared byte for byte, and an exact-directory
check rejects missing, extra, symlinked, non-regular, malformed, or reordered
entries. The final `gh release create` command receives all 13 filenames
explicitly and contains no asset glob.

The review also found that the former release job performed source checkout,
Lean verification, arbitrary repository tooling, attestation, and publication
under one workflow-wide write token. The new `verify-and-package` job has only
read permission. A distinct tag-only `publish` job receives write/OIDC rights,
does not check out or execute repository code, validates the transferred
candidate inline, and scopes `GH_TOKEN` to the final upload step. Manual dispatch
can verify but cannot publish.

Workflow tests now fail if write permission moves to workflow scope, if the two
jobs collapse, if privileged source checkout or repository-script execution is
introduced, or if an explicit asset path is replaced by a wildcard. Public Lean
statements, proof pins, and claims remain unchanged.
