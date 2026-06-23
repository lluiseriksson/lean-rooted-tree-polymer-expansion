# Reproducibility

## Local source-package preflight

```bash
make docs-setup
make verify-nonlean
make package-determinism
```

This performs:

1. focused repository-tooling tests plus Python and shell syntax checks;
2. generation of the continuous article from the canonical section manifest;
3. a strict MkDocs build;
4. project-identity, source-blob, statement-fingerprint, dependency-lock,
   Python-lock, source-manifest, proof-DAG, paper-manifest, reference, metadata,
   accessibility, link, workflow, agent-index, placeholder, and source-tree
   audits;
5. two byte-identical release-evidence builds and a clean-room archive test.

The ordinary path does **not** run `lake update` and does not require a local
Lean rebuild. Source changes must be followed by `make manifest`; `make static`
rejects a stale committed manifest rather than repairing it implicitly.

## Authoritative Lean gate

GitHub Actions supplies the expected pinned Linux environment and cache. The
pinned Lean action is configured with automatic feature detection disabled and
performs exactly one build of `MarkedRootedClosure`, followed by its pinned Lean
environment checker. The next workflow step runs:

```bash
make lean-oracle
```

This checks that every public endpoint reports exactly the documented axiom set.
The workflow audit rejects an implicit Lean-action build policy, removal of the
environment checker, or a second `make lean` invocation after the action has
already compiled the package.

A maintainer may deliberately reproduce the complete gate locally:

```bash
make lean
# or: make verify
```

`make lean-build` and `make lean-oracle` execute through
`scripts/run_lean_gate.py`. Its dependency-free process runner creates an
isolated process group and terminates the complete Lean/Lake descendant tree on
an internal timeout, terminal interrupt, or loss of the invoking parent. It
also requires `lake-manifest.json` to remain byte-identical. Default timeouts can
be changed without bypassing supervision:

```bash
make lean LEAN_BUILD_TIMEOUT=5400 LEAN_ORACLE_TIMEOUT=900
```

On oracle failure, `.oracle.log` is retained for diagnosis. On success it is
removed. The transient log is intentionally excluded from the release source
inventory.

## Explicit supervised sequence

```bash
make lean-build
make lean-oracle
make test
make syntax
make docs
make static
```

Avoid running long raw `lake` commands under an external timeout: a wrapper that
kills only its direct child can leave Lean workers alive. The supervised Make
targets handle descendant cleanup themselves.

## Python documentation environment

`requirements-docs.txt` records the four direct dependencies. The executable
reproducible environment is the exact transitive `requirements-docs.lock`, used
by local setup, CI, Pages, Docker, and the dev container. The lock audit rejects
range constraints, canonical-name duplicates, missing direct packages, and the
superseded CFF/minifier dependency chain.

## Refreshing dependency locks

Only maintainers intending to update a Lean dependency should run:

```bash
make lock-refresh
git diff -- lake-manifest.json lakefile.lean archive/UPSTREAM.lock
```

A lock refresh also runs under the process-tree supervisor; its default
`LAKE_UPDATE_TIMEOUT` is thirty minutes. A lock change requires a dedicated
review, refreshed source Git blob IDs and
statement excerpts where applicable, a fresh oracle inspection, and a
cold-cache Lean CI run.

## Container verification

```bash
docker build -t lean-rooted-tree-polymer-expansion .
docker run --rm -v "$PWD:/workspace" -w /workspace \
  lean-rooted-tree-polymer-expansion make verify
```

The Dockerfile pins the elan installer script by commit and verifies its Git
blob ID. The Lean toolchain itself is pinned separately in `lean-toolchain`.
The first build requires network access to retrieve exact Git objects unless the
Lake cache is already populated.

## Expected oracle boundary

Each public endpoint must report exactly:

```text
propext
Classical.choice
Quot.sound
```

The audit rejects missing reports, additional axioms, `sorry`, `admit`,
`sorryAx`, and project-local axiom declarations.

## Deterministic release

```bash
make package-determinism
```

The command produces exactly 13 files:

- a source-only deterministic ZIP, SPDX 2.3 SBOM, CycloneDX 1.5 SBOM,
  deterministic build information, deterministic in-toto Statement v1 / SLSA
  declaration, and release evidence index;
- one canonical `.sha256` sidecar for each of those six primary files;
- one ordered aggregate SHA-256 file covering the six primary files.

`scripts/release_inventory.py` defines that set once for generators,
determinism, verification, and documentation. The evidence set is built twice
and must match byte-for-byte. The verifier rejects missing or unexpected
release-directory entries and compares every sidecar and aggregate byte for
byte before it checks the deeper artifact semantics. The verifier
checks archive path safety, duplicate/non-canonical aliases,
file/directory conflicts, case/Unicode collisions, portable names, file types,
member and total sizes, the archive-local manifest, required files, proof pins,
SBOM metadata and Python lock coverage, the exact non-execution-bound
provenance policy and resolved dependency set, release-index records, and every
recorded digest.
`make smoke-release` then extracts the ZIP into a temporary clean-room tree and
reruns dependency-free audits and tests under the same process-tree supervisor.

The deterministic in-toto file binds subjects, dependencies, the source inputs,
and the declared release recipe. It explicitly sets `executionBound: false` and
requires a hosted attestation; it does not claim that a particular GitHub run
already executed. Tagged releases add separate GitHub build-provenance
attestations as the execution-bound evidence.

## Privilege-separated tagged publication

The release workflow builds the candidate in a `contents: read` job. Only after
Lean/oracle and deterministic packaging succeed is the exact `release/`
directory transferred to a separate semantic-tag-only job. That publisher has
write/OIDC permissions but does not check out source or execute repository
scripts. It independently validates the 13 filenames, sidecars, aggregate
ordering, and release-index identity, then attests and uploads explicit paths.
The workflow audit rejects wildcard publication and any collapse of this
boundary.

## Scheduled drift detection

The monthly `scheduled-maintenance` workflow disables the Lean GitHub cache,
builds the wrapper once, runs the environment checker and exact oracle,
recreates deterministic release evidence, and smoke-tests the archive. This
detects dependency-service or runner-image drift without changing any source
lock.

## Offline review boundary

The repository contains the article, public theorem statements, signature
fingerprints, source Git blob IDs, source locks, theorem excerpts, and release
tooling. A fresh Lean build still requires the pinned dependencies or a
populated cache. This is an explicit network requirement, not an offline-build
claim.
