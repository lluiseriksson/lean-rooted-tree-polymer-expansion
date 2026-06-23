# What this project is

!!! note "Archived final state"

    The repository is closed at `v2.4.3`. It is preserved as a reproducible
    Lean 4 proof artifact and documentation site, not as an active research
    programme or an ongoing publication claim.

This project is a compact, reviewable publication artifact for one precise
piece of constructive mathematical physics: a finite rooted-tree summation that
preserves enough geometric information to retain decay in an exact target
polymer.

The repository combines four layers:

1. **Mathematics.** A normalized bound on rooted child-factorial tree weights,
   a parent-normalized incompatibility kernel, fixed-tree leaf elimination, and
   target-preserving composition.
2. **Formal verification.** Lean 4 aliases expose three stable theorem endpoints
   whose proofs live in one immutable upstream revision.
3. **Scholarly exposition.** The article, references, theorem map, assumptions,
   and limitations are maintained under `docs/` and deployed as this site.
4. **Artifact engineering.** Dependency locks, CI, deterministic release
   archives, checksums, metadata, an SPDX SBOM, and evaluator instructions make
   the result inspectable rather than merely downloadable.

## The core design constraint

Two kinds of information must not be discarded too early:

- the exact target union $Y$, needed to extract modified-metric decay; and
- parent--child incompatibility, needed for the local rooted-tree recursion.

The proof therefore follows the order

$$
\text{exact union}
\longrightarrow
\text{target decay}
\longrightarrow
\text{marked root}
\longrightarrow
\text{fixed-tree elimination}
\longrightarrow
\text{tree-profile summation}.
$$

Reversing the first two stages can preserve a global norm bound while losing
the target-sensitive exponential that later multiscale arguments need.

## Intended audience

The repository is designed for reviewers and researchers working in Lean,
cluster expansions, polymer models, constructive field theory, renormalization
group methods, or formalized mathematics. It is also structured so an artifact
evaluator can reproduce the result without reading the entire upstream
Yang--Mills development.

The intended use is archival review, reuse of the small public Lean interface,
and inspection of the release evidence. New mathematical claims should be made
in a separate project rather than by extending this closed artifact.
