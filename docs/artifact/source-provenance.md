# Source provenance

## Locked proof source

| Component | Locked value |
|---|---|
| Upstream repository | `lluiseriksson/THE-ERIKSSON-PROGRAMME` |
| Upstream commit | `4e45246aa109671d25fcd01ba1abf7bc3f8506d1` |
| Upstream commit message | `feat(RG): characterize flat harmonic kernel` |
| `RootedLeafSummation.lean` Git blob | `1415686403c26536da8736a9021237773c7467dc` |
| `AppendixFSecondUrsellLeafSummation.lean` Git blob | `0307d11b95d4385d4ea39067290e7eec929cd7f6` |
| Lean toolchain | `leanprover/lean4:v4.29.0-rc6` |
| Mathlib commit | `07642720480157414db592fa85b626dafb71355b` |
| Elan installer script commit | `b6cec7e10fe4965a605aaf60d1cb4a5837f0462b` |
| Elan installer script Git blob | `ab8c346be2d665b2c77a6eba0dc2338c43413a9c` |

The authoritative machine-readable records are
[`archive/UPSTREAM.lock`](https://github.com/lluiseriksson/lean-rooted-tree-polymer-expansion/blob/main/archive/UPSTREAM.lock)
and
[`archive/theorem-manifest.json`](https://github.com/lluiseriksson/lean-rooted-tree-polymer-expansion/blob/main/archive/theorem-manifest.json).

## Statement fingerprints

Each public wrapper theorem has a SHA-256 fingerprint computed from its
whitespace-normalized Lean declaration, excluding the proof term. This detects
changes to binders, hypotheses, constants, or conclusions even when theorem
names remain unchanged.

| Public endpoint | Signature SHA-256 |
|---|---|
| `normalizedRootedChildFactorialTreeBound` | `65481a73cfd74d6e9a35000c8c657820252b5e10b1df074e18a08ec2b27fde84` |
| `markedRootLeafGeometricBound` | `eed559375b1557b93cbec8a9f9038430b5360b854bac9da39f2faf5e2f08f2a3` |
| `targetPreservingWeightedTreeBound` | `b9e729583eccb273791e763f5d98bd60f575361769e180552ee383097b537e57` |

The fingerprints are checked by `scripts/check_theorem_manifest.py`; the
extractor is `scripts/lean_signatures.py` and has dedicated regression tests.
They are traceability evidence, not a substitute for Lean kernel compilation.

## Verification route

1. Lake resolves the upstream repository at the exact commit.
2. The companion imports the two source modules containing the proofs.
3. The theorem manifest binds each endpoint to an upstream theorem, source
   path, Git blob, source excerpt, article page, and public signature hash.
4. Each public theorem is a transparent term proof applying one upstream
   theorem.
5. `MarkedRootedClosure/Oracle.lean` prints the axioms of every public endpoint;
   the audit requires exactly `propext`, `Classical.choice`, and `Quot.sound`.
6. Short statement excerpts under `vendor/upstream-excerpts/` permit offline
   comparison without pretending to vendor the complete proof dependency.
7. Static and release audits reject drift among locks, manifests, wrappers,
   excerpts, documentation, SBOMs, and release evidence.

## Why the complete upstream is not copied

Duplicating a rapidly evolving proof repository would create two sources of
truth and make security updates harder. The companion instead uses an immutable
Git commit and records the exact source Git blobs used by the public endpoints.
A first kernel rebuild therefore requires Git access or a pre-populated Lake
cache; subsequent builds are local.
