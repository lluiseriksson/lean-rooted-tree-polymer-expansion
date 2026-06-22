#!/usr/bin/env python3
"""Synchronize repository URLs and release naming after a GitHub repo rename.

The script defaults to a dry run. Use --apply only after the repository has
actually been renamed in GitHub Settings.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from project_config import ROOT, load_project, repository_url, site_url

TEXT_SUFFIXES = {
    "", ".md", ".txt", ".json", ".yml", ".yaml", ".toml", ".lean",
    ".py", ".sh", ".cff", ".bib", ".css", ".js",
}
EXCLUDED_PARTS = {
    ".git", ".lake", "site", "release", ".venv", ".venv-docs",
    "__pycache__", "vendor",
}
EXCLUDED_FILES = {"MANIFEST.sha256"}


def valid_slug(value: str) -> bool:
    return bool(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner", required=True)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--apply", action="store_true", help="write changes")
    args = parser.parse_args()

    if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?", args.owner):
        raise SystemExit(f"invalid GitHub owner: {args.owner!r}")
    if not valid_slug(args.slug):
        raise SystemExit(f"invalid repository slug: {args.slug!r}")

    project = load_project()
    old_owner = project["repository_owner"]
    old_slug = project["repository_slug"]
    if old_owner == args.owner and old_slug == args.slug:
        print("repository identity is already synchronized")
        return

    old_repo = repository_url(project)
    old_site = site_url(project)
    old_full = f"{old_owner}/{old_slug}"
    new_repo = f"https://github.com/{args.owner}/{args.slug}"
    new_site = f"https://{args.owner}.github.io/{args.slug}/"
    new_full = f"{args.owner}/{args.slug}"

    replacements = [
        (old_site, new_site),
        (old_repo, new_repo),
        (old_full, new_full),
        (f"{old_slug}-v", f"{args.slug}-v"),
        (f'"name": "{old_slug}"', f'"name": "{args.slug}"'),
        (f"-t {old_slug} ", f"-t {args.slug} "),
        (f" {old_slug} make", f" {args.slug} make"),
    ]

    changed: list[Path] = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.name in EXCLUDED_FILES:
            continue
        rel = path.relative_to(ROOT)
        if any(part in EXCLUDED_PARTS for part in rel.parts):
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            before = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        after = before
        for old, new in replacements:
            after = after.replace(old, new)
        if after != before:
            changed.append(rel)
            if args.apply:
                path.write_text(after, encoding="utf-8")

    project_path = ROOT / "project.json"
    project["repository_owner"] = args.owner
    project["repository_slug"] = args.slug
    if args.slug == project.get("recommended_repository_slug"):
        project["rename_status"] = "adopted"
        project["previous_repository_slug"] = old_slug
    else:
        project["rename_status"] = "proposed"
    changed.append(project_path.relative_to(ROOT))
    if args.apply:
        project_path.write_text(
            json.dumps(project, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    mode = "APPLY" if args.apply else "DRY RUN"
    print(f"repository rename synchronization ({mode})")
    print(f"  {old_full} -> {new_full}")
    print(f"  {old_site} -> {new_site}")
    for rel in sorted(set(changed), key=str):
        print(f"  {rel}")
    if not args.apply:
        print("No files were changed. Re-run with --apply after the GitHub rename.")
    else:
        print("Run: make static && make docs")


if __name__ == "__main__":
    main()
