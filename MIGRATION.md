# Migration to v2.4.2

Version 2.4.2 preserves the v2.4.1 mathematical interface and release evidence
format while replacing unsupervised local Lean/Lake execution and duplicate CI
builds with an explicit single-build gate.

## Replacement procedure

Use a delete-aware copy so obsolete files and generated caches do not survive:

```bash
rsync -a --delete --exclude='.git/' \
  /path/to/lean-rooted-tree-polymer-expansion-v2.4.2/ ./
make docs-setup
make verify-nonlean
make package-determinism
```

Push without tagging. GitHub Actions performs the authoritative Lean build in
the pinned Linux environment and then runs `make lean-oracle`. Tag `v2.4.2` only
after Lean, static/docs, package reproducibility, clean-room, and Pages checks
are green.

## Local Lean verification

A maintainer who intentionally wants the full local gate should run:

```bash
make lean
```

Do not invoke long-running `lake build` commands through an external timeout.
The Make target uses `scripts/run_lean_gate.py`, which terminates the complete
process tree on timeout, interrupt, or parent loss. The defaults can be adjusted
without bypassing supervision:

```bash
make lean LEAN_BUILD_TIMEOUT=5400 LEAN_ORACLE_TIMEOUT=900
```

`make lock-refresh` and `make clean` also route their Lake subprocesses through
the same supervisor. A command that exits while leaving a background descendant
is treated as a failure and that descendant group is terminated.

## CI workflow change

The pinned Lean action now builds `MarkedRootedClosure` exactly once and runs
the pinned Lean environment checker. Workflows must keep the explicit policy
block and follow it with `make lean-oracle`; the workflow audit rejects a return
to implicit auto-configuration, removal of `leanchecker: true`, or a second full
Lean build.

## Release evidence boundary

The deterministic local in-toto statement is a reproducible declaration of
subjects, source inputs, dependencies, and required external gates. It is not an
execution attestation. Tagged releases continue to publish separate GitHub
build-provenance attestations for execution-bound evidence. The release verifier
and JSON Schema require this boundary exactly and reject metadata that claims a
hosted execution occurred locally.
