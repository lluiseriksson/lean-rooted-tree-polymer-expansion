# Repository rename proposal

## Recommendation

Rename

```text
lluiseriksson/lean-rooted-tree-polymer-expansion
```

to

```text
lluiseriksson/lean-rooted-tree-polymer-expansion
```

The corresponding Pages URL becomes:

```text
https://lluiseriksson.github.io/lean-rooted-tree-polymer-expansion/
```

## Why this name is clearer

- **`lean`** tells readers that the result is machine-checked.
- **`rooted-tree`** names the combinatorial proof engine.
- **`polymer-expansion`** identifies the mathematical setting recognized by
  statistical mechanics and constructive field theory readers.

The old name records an internal proof phrase—“marked rooted closure”—but does
not tell an external reader what is being closed or that the repository is a
formalization.

## What does not change

The article title and the stable Lean namespace `MarkedRootedClosure` remain
unchanged. Keeping the namespace avoids breaking imports, theorem references,
and archived citations.

## Safe migration

1. Merge and verify this release under the current repository name.
2. In GitHub, open **Settings → General → Repository name** and rename the repo.
3. In a clean checkout of the renamed repository, run:

   ```bash
   python3 scripts/rename_repository.py \
     --owner lluiseriksson \
     --slug lean-rooted-tree-polymer-expansion \
     --apply
   make static
   ```

4. Commit the generated URL and metadata changes.
5. In **Settings → Pages**, keep **GitHub Actions** as the deployment source and
   rerun the documentation workflow.
6. Update the repository “About” description and website field.
7. Verify the new Pages URL, badges, edit links, citation metadata, release
   prefix, issue forms, and Zenodo integration.

GitHub redirects ordinary repository URLs after a rename, but a project Pages
URL should be treated as a new public URL. Existing citations should therefore
continue to include a versioned release or DOI when one is available.

## Suggested GitHub “About” text

> Lean 4 formalization of target-preserving rooted-tree leaf summation for
> polymer cluster expansions with holes, with an integrated article and a
> reproducible proof artifact.
