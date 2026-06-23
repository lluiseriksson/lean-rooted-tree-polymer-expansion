# Verification contract

A release is accepted only when every layer below passes on the exact tagged
source tree.

| Layer | Command or workflow | What it checks |
|---|---|---|
| Tooling tests | `make test` | Metadata, article assembly, statement fingerprints, exact oracle parsing, process supervision, workflow policy, references, agent index, source-inventory drift, release metadata, and malicious-archive regression cases |
| Local non-Lean preflight | `make verify-nonlean` | Tooling tests, syntax, strict documentation, project identity, locks, source-manifest freshness, source Git blobs, theorem map, paper manifest, references, links, workflows, schemas, metadata, accessibility, placeholders, and the no-standalone-PDF rule |
| Lean kernel | pinned `lean-action` build and environment check followed by `make lean-oracle` | One compilation of the wrapper in GitHub Actions, an independent environment check, and exact oracle equality with the documented classical axiom set |
| Optional local Lean | `make lean` | The same build and oracle through a timeout-, interrupt-, and parent-loss-aware process-tree supervisor |
| Deterministic package | `make package-determinism` | Byte-identical source ZIPs, per-file and aggregate checksums, SPDX/CycloneDX SBOMs, deterministic build information, local in-toto declaration, and release index |
| Clean-room archive | `make smoke-release` | Safe extraction followed by the dependency-free audit runner inside the archive, with descendant cleanup on timeout |
| Monthly maintenance | `maintenance.yml` | Cold-cache single Lean build, environment check, exact oracle, full non-Lean verification, deterministic packaging, and archive smoke test |
| Tagged release | `release.yml` | Canonical-repository guard, tag/version agreement, single Lean build, environment check, exact oracle, deterministic evidence, hosted provenance attestations, and release publication |

## Kernel claim

The public theorem endpoints are exact aliases of the pinned upstream proofs.
For every endpoint, the oracle must report exactly:

```text
propext
Classical.choice
Quot.sound
```

An additional axiom fails the build. Missing oracle output, `sorry`, `admit`,
`sorryAx`, or project-local axioms also fail verification.

The CI action is configured explicitly with automatic feature detection off and
`build-args: MarkedRootedClosure`; a subsequent full `make lean` would duplicate
the kernel build and is forbidden by the workflow audit. CI runs only
`make lean-oracle` after the action build.

## Process-lifecycle claim

Local `make lean-build` and `make lean-oracle` launch their commands in isolated
process groups. Timeout, SIGINT, SIGTERM, SIGHUP, or disappearance of the
invoking parent terminates the complete descendant tree and escalates to a
forced kill after a bounded grace period. The same runner protects clean-room
and deterministic-evidence subprocesses.

`lake-manifest.json` is snapshotted before each local Lean phase and must remain
byte-identical afterward, whether or not the source tree contains `.git`.

## Statement and source identity

The theorem manifest records:

- the public and upstream theorem names;
- the exact upstream source path and Git blob ID;
- a SHA-256 fingerprint of the normalized public Lean statement;
- a hashed offline source-statement excerpt;
- the article page and explicit negative claims boundary.

These records detect semantic drift that a theorem-name-only audit would miss.

## Publication claim

The article is maintained under `docs/paper/`. The continuous article view is
generated from those same files. A separate manuscript PDF or duplicate LaTeX
manuscript is forbidden in the source release.

## Provenance boundary

The deterministic `.intoto.jsonl` file is reproducible source-tooling metadata.
It binds subjects, dependencies, source inputs, the release recipe, and required
external Lean gates, but sets `executionBound: false`. It is not evidence that a
specific hosted run occurred. Tagged releases therefore require separate GitHub
build-provenance attestations, which supply the execution-bound claim.

## Release evidence

Every release publishes a deterministic source ZIP, sidecars, aggregate
checksums, SPDX 2.3 and CycloneDX 1.5 SBOMs, deterministic build information, a
release index, the deterministic in-toto declaration, and GitHub hosted
attestations.

See [Release evidence](release-evidence.md) for verification commands.
