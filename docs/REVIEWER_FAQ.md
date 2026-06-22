# Reviewer FAQ

## Is the `4^n` bound new?

No priority claim is made for the elementary central-binomial estimate. The
contribution is the machine-checked assembly in the target-preserving
with-holes second-Ursell pipeline, including the parent-normalized moment
recursion and exact proof order.

## Why is the target-preserving order important?

Once the exact union `Y` is erased, the enlarged marked-root sum contains no
variable from which `exp(-rate * m(Y))` can be derived. The target factor must be
extracted inside the exact-union fiber first.

## Why not use a global polymer mass?

A global unpinned sum can depend on the volume and discards parent-child
locality. The fixed-tree recursion uses incompatible child sums pinned through
the parent and ends with a root-pinned moment.

## Is this a Yang-Mills theorem?

It is a theorem in infrastructure motivated by constructive Yang-Mills. It does
not define or estimate the concrete gauge fluctuation activity. The paper and
artifact state this explicitly.

## Why does the companion depend on a larger pinned repository?

The full proofs are already part of a larger machine-checked programme. The
companion provides stable publication-facing endpoints and immutable source
pins without duplicating the entire project. Short exact statement excerpts are
included for offline review.

## Is the paper reproducible without network access?

The PDF, signatures, hashes, and excerpts are reviewable offline. A first Lean
kernel rebuild needs the pinned Git dependencies or a pre-populated Lake cache.
After dependency resolution, subsequent builds are local.

## What should a reviewer run first?

```bash
lake update
lake build MarkedRootedClosure
lake env lean MarkedRootedClosure/Oracle.lean
python3 scripts/check_artifact.py
```
