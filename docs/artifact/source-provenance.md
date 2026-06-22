# Source provenance

## Locked proof source

| Component | Locked value |
|---|---|
| Upstream repository | `lluiseriksson/THE-ERIKSSON-PROGRAMME` |
| Upstream commit | `4e45246aa109671d25fcd01ba1abf7bc3f8506d1` |
| Upstream commit message | `feat(RG): characterize flat harmonic kernel` |
| Lean toolchain | `leanprover/lean4:v4.29.0-rc6` |
| Mathlib commit | `07642720480157414db592fa85b626dafb71355b` |

The authoritative machine-readable records are
[`archive/UPSTREAM.lock`](https://github.com/lluiseriksson/marked-rooted-closure/blob/main/archive/UPSTREAM.lock)
and
[`archive/theorem-manifest.json`](https://github.com/lluiseriksson/marked-rooted-closure/blob/main/archive/theorem-manifest.json).

## Verification route

1. Lake resolves the upstream repository at the exact commit.
2. The companion imports the two source modules containing the proofs.
3. Each public theorem is an exact term proof applying one upstream theorem.
4. `MarkedRootedClosure/Oracle.lean` prints the axioms of every public endpoint.
5. Short statement excerpts under `vendor/upstream-excerpts/` permit offline
   comparison without pretending to vendor the complete proof dependency.
6. `scripts/check_artifact.py` rejects drift between the lock, Lake file,
   theorem manifest, documentation, and wrappers.

## Why the complete upstream is not copied

Duplicating a rapidly evolving proof repository would create two sources of
truth and make security updates harder. The companion instead uses an immutable
Git commit and retains exact theorem statements locally. A first kernel rebuild
therefore requires Git access or a pre-populated Lake cache; subsequent builds
are local.
