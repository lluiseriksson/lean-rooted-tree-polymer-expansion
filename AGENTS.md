# Agent instructions

1. Preserve the exact theorem statements and immutable upstream pin.
2. Run `make static` after every documentation or metadata change.
3. Run `make verify` before tagging a release.
4. Never introduce `sorry`, `admit`, or project-local axioms.
5. Do not claim a Yang--Mills mass gap, `hRpoly`, continuum construction, or
   cardinal-infinity theorem.
6. Keep the paper under `docs/paper/`; do not reintroduce a tracked standalone
   PDF or a second manuscript source.
7. Update the theorem manifest, paper, theorem map, and oracle together when a
   public endpoint changes.
8. A release is not verified until GitHub Actions has completed a clean Lean
   kernel build.
