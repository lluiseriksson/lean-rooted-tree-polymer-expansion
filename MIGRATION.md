# Migration to v2.4.3

Version 2.4.3 preserves the v2.4.2 mathematical interface, exact theorem
statements, proof-source pins, and 13-file evidence format. The change is at the
publication boundary: release construction now runs with read-only repository
permission, while a separate tag-only job receives the minimum permissions
needed to attest and publish an already verified candidate.

## Replace, do not overlay

Use a delete-aware copy so obsolete files and generated caches do not survive:

```bash
rsync -a --delete --exclude='.git/' \
  /path/to/lean-rooted-tree-polymer-expansion-v2.4.3/ ./
make docs-setup
make verify-nonlean
make package-determinism
```

The local package gate must produce exactly 13 regular files in `release/`:
six checksum subjects, six canonical sidecars, and one aggregate checksum.
Unexpected, missing, symlinked, reordered, or checksum-inconsistent entries are
fatal.

Push without tagging. GitHub Actions performs the authoritative Lean build and
oracle audit in the pinned Linux environment. Tag `v2.4.3` only after the Lean,
leanchecker, documentation, deterministic package, clean-room, provenance, and
Pages checks are green.

## Publication boundary

The tagged workflow transfers the verified `release/` directory into a separate
publisher. The publisher does not check out the repository and must not run
repository scripts. It validates the exact asset inventory using an inline,
dependency-free check and passes all 13 filenames explicitly to the release
command; broad `release/*` globs are forbidden.
