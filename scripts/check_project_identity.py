#!/usr/bin/env python3
"""Validate the adopted repository identity across human and machine metadata."""
from __future__ import annotations

import json
from pathlib import Path

from project_config import ROOT, load_project, repository_full_name, repository_url, site_url
from source_inventory import collect_source_files

project = load_project()
version = project["version"]
repo_full = repository_full_name(project)
repo = repository_url(project)
site = site_url(project)
slug = project["repository_slug"]
previous = project.get("previous_repository_slug")

must_contain = {
    "README.md": [project["site_name"], repo, site, slug, version],
    "mkdocs.yml": [project["site_name"], project["site_tagline"], repo, site, repo_full],
    "CITATION.cff": [version, repo, site, project["artifact_title"]],
    "CITATION.bib": [version, repo],
    "codemeta.json": [version, repo, site, project["site_name"]],
    ".zenodo.json": [version, project["artifact_title"]],
    "archive/theorem-manifest.json": [version, project["upstream_commit"], repo, site],
    "docs/publication/submission-metadata.yaml": [version, project["artifact_title"]],
    "REPOSITORY_HISTORY.md": [repo_full, site, "MarkedRootedClosure"],
    "docs/maintainers/repository-history.md": [repo_full, site, "MarkedRootedClosure"],
}
for rel, needles in must_contain.items():
    path = ROOT / rel
    if not path.is_file():
        raise SystemExit(f"identity audit: missing {rel}")
    text = path.read_text(encoding="utf-8")
    for needle in needles:
        if needle not in text:
            raise SystemExit(f"identity audit: {needle!r} missing from {rel}")

for rel in ("project.json", "codemeta.json", ".zenodo.json", "archive/theorem-manifest.json"):
    json.loads((ROOT / rel).read_text(encoding="utf-8"))

if (ROOT / "REPOSITORY_RENAME.md").exists() or (ROOT / "docs/maintainers/rename-repository.md").exists():
    raise SystemExit("obsolete rename-proposal files must be removed after adoption")

old_urls = []
if previous:
    old_urls = [
        f"https://github.com/{project['repository_owner']}/{previous}",
        f"https://{project['repository_owner']}.github.io/{previous}/",
    ]
for path in collect_source_files(ROOT):
    rel = path.relative_to(ROOT)
    if path.suffix.lower() in {".png", ".jpg", ".jpeg"}:
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    for old_url in old_urls:
        if old_url in text:
            raise SystemExit(f"stale pre-rename URL in {rel}: {old_url}")

readme = (ROOT / "README.md").read_text(encoding="utf-8")
for stale in (
    "Uploading this v2 tree",
    "The existing GitHub repository contains the previous PDF-based bundle",
    "paper/main.pdf",
    "paper/main.tex",
    "recommended public name",
):
    if stale in readme:
        raise SystemExit(f"stale publication language in README: {stale!r}")

print("project identity audit: OK")
print(f"current repository: {repo_full}")
print("rename status: adopted; Lean namespace preserved")
