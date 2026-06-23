# Release notes: v2.4.2

Version 2.4.2 is an execution-safety and CI-efficiency maintenance release. It
preserves the exact three public Lean theorem statements, upstream proof commit,
Lean toolchain, Mathlib commit, oracle boundary, and mathematical claims boundary
from v2.4.1.

## Supervised Lean/Lake execution

Local Lean verification now runs through a dependency-free supervisor. Every
command receives its own process group. A timeout, terminal interrupt, or loss
of the invoking parent terminates the complete descendant tree, first
cooperatively and then forcibly if necessary. This prevents timed-out `lake` or
`lean` children from continuing to consume CPU and memory after their caller has
exited.

Cleanup is checked independently of the immediate child: even if that child
exits on `SIGTERM` while a worker ignores it, the remaining process group is
forcibly removed. A command that returns success while leaving a background
descendant is rejected. The explicit lock-refresh and best-effort clean targets
use the same supervisor.

The supervisor also snapshots `lake-manifest.json` before each build or oracle
phase and rejects any byte-level lock drift, including in source archives that
do not contain Git metadata. Partial oracle output is retained on failure and
removed after a successful exact-axiom audit.

## One Lean build per CI job

The pinned `leanprover/lean-action` invocation is now configured explicitly with
`auto-config: false`, `build: true`, `build-args: MarkedRootedClosure`, and
`leanchecker: true`. GitHub Actions therefore performs the kernel build once,
runs the pinned environment checker, saves the resulting cache, and then runs
only `make lean-oracle`. Previous workflows allowed the action's automatic build
and `make lean` to compile the same target twice.

The static/docs, Pages, maintenance, and release workflows use the new
`make verify-nonlean` entrypoint. Local reviewers can run the same non-Lean
preflight and leave the authoritative kernel gate to the expected cached Linux
CI environment.

## Process-safe release tooling

The clean-room archive command and deterministic evidence builder now use the
same whole-process-tree supervision. Composite Make targets invoke their stages
sequentially even when a caller supplies `-j`, avoiding races between generated
article output and static checks. The transient `.oracle.log` is excluded from
the source manifest while remaining available after a failed oracle audit.

## Provenance boundary

The deterministic in-toto statement now identifies itself as a reproducible
source-tooling declaration with `executionBound: false` and explicitly requires
a hosted attestation. It binds subjects, dependencies, and the declared release
recipe without claiming that a particular GitHub release workflow already ran.
GitHub's hosted build-provenance attestations remain the execution-bound evidence
for tagged artifacts.

The committed JSON Schema and release verifier now enforce that distinction,
including the exact builder identity, source-input digests, five resolved
dependencies, release recipe, and two required external Lean gates.

## Mathematical scope

The release formalizes finite rooted-tree and target-sensitive second-Ursell
bounds. It does not prove the model-specific raw Yang--Mills activity estimate,
`hRpoly`, a continuum construction, Osterwalder--Schrader reconstruction, or a
mass gap theorem.
