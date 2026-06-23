# Verification contract

A release is accepted only when every layer below passes on the exact tagged
source tree.

| Layer | Command or workflow | What it checks |
|---|---|---|
| Tooling tests | `make test` | Metadata, article assembly, statement fingerprints, exact oracle parsing, workflow policy, references, agent index, release metadata, and malicious-archive regression cases |
| Static artifact audit | `make static` | Project identity, dependency locks, source Git blobs, theorem map, paper manifest, references, links, workflows, schemas, metadata, placeholders, and the no-standalone-PDF rule |
| Documentation | `make docs` | Strict MkDocs build from canonical Markdown article sources |
| Lean kernel | `make lean` | Compilation of the wrapper and exact oracle equality with the documented classical axiom set |
| Deterministic package | `make package-determinism` | Byte-identical source ZIPs, per-file and aggregate checksums, SPDX/CycloneDX SBOMs, deterministic build information, and release index |
| Clean-room archive | `make smoke-release` | Safe extraction followed by the single-process dependency-free audit runner inside the archive |
| Monthly maintenance | `maintenance.yml` | Cold-cache Lean rebuild, full documentation/static verification, deterministic packaging, and archive smoke test |
| Tagged release | `release.yml` | Canonical-repository guard, tag/version agreement, full verification, artifact upload, GitHub provenance attestations, and release publication |

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

## Release evidence

Every release publishes a deterministic source ZIP, sidecars, aggregate
checksums, SPDX 2.3 and CycloneDX 1.5 SBOMs, deterministic build information, a
release index, and GitHub build-provenance attestations.

See [Release evidence](release-evidence.md) for verification commands.
