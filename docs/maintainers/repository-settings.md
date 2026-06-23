# Recommended GitHub repository settings

The source tree cannot enforce repository-level controls. Apply these settings
manually after uploading a release tree.

## General

- Default branch: `main`.
- Disable wiki and projects unless they are actively maintained.
- Enable issues and discussions only when the maintainer intends to triage them.
- Allow squash merges; disable merge commits for a linear publication history.
- Automatically delete head branches after merge.

## Branch protection for `main`

Require a pull request and require the following checks before merge:

- `Tooling tests, static audit, and strict documentation`;
- `Deterministic package, dual SBOMs, and clean-room smoke test`;
- `Lean kernel and oracle verification`;
- `dependency-review / review` when dependency files change.

Also require:

- the branch to be up to date before merge;
- conversation resolution;
- at least one approving review for third-party contributions;
- dismissal of stale approvals when theorem wrappers, locks, workflows, or
  article claims change;
- no force pushes and no branch deletion.

## GitHub Pages

Set Pages deployment source to **GitHub Actions**. The privileged Pages workflow
is guarded so it runs only in the canonical repository.

## Releases

- Create tags only after `make release` and all `main` checks pass.
- Prefer signed annotated tags where the maintainer's signing setup is
  available.
- Protect the `v*` tag pattern if the repository plan supports tag protection.
- Keep GitHub artifact attestations enabled.
- Do not upload a separately maintained manuscript PDF; the article remains in
  the documentation tree.

## Security

- Enable private vulnerability reporting.
- Enable Dependabot alerts and security updates.
- Enable secret scanning and push protection where available.
- Review monthly scheduled clean-room verification failures promptly.

## Release acceptance

A release is accepted only when the tag, `project.json`, `CITATION.cff`, release
index, source ZIP, SBOMs, and generated checksums all agree on the same version.
