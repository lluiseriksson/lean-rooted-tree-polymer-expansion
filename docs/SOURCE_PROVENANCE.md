# Source provenance

## Upstream proof source

- Repository: `lluiseriksson/THE-ERIKSSON-PROGRAMME`
- Commit: `83d18a113e3fa22ada23b13361fb84015a1c80ed`
- Commit message: `feat(RG): assemble gauge-fixed covariance`
- Lean toolchain: `leanprover/lean4:v4.29.0-rc6`
- Mathlib commit: `07642720480157414db592fa85b626dafb71355b`

## Relevant source blobs

| File | Git blob |
|---|---|
| `YangMills/KP/RootedLeafSummation.lean` | `1415686403c26536da8736a9021237773c7467dc` |
| `YangMills/RG/AppendixFSecondUrsellLeafSummation.lean` | `0307d11b95d4385d4ea39067290e7eec929cd7f6` |

## Verification route

1. Lake resolves the upstream repository at the exact commit.
2. The companion imports the two source modules.
3. Each public theorem is an exact term proof applying one upstream theorem.
4. `MarkedRootedClosure/Oracle.lean` prints the axioms of the public endpoints.
5. Short statement excerpts are included under `vendor/upstream-excerpts/` for
   offline comparison.
