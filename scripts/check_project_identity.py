#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

from project_config import ROOT, load_project, repository_full_name, repository_url, site_url

project = load_project()
version = project["version"]
repo_full = repository_full_name(project)
repo = repository_url(project)
site = site_url(project)
recommended = project["recommended_repository_slug"]

slug_re = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
for key in ("repository_slug", "recommended_repository_slug"):
    value = project[key]
    if not slug_re.fullmatch(value):
        raise SystemExit(f"invalid repository slug in project.json: {key}={value!r}")
status = project.get("rename_status")
if status not in {"proposed", "adopted"}:
    raise SystemExit("rename_status must be proposed or adopted")
if status == "proposed" and recommended == project["repository_slug"]:
    raise SystemExit("a proposed repository slug must differ from the current slug")
if status == "adopted" and recommended != project["repository_slug"]:
    raise SystemExit("an adopted repository slug must equal the current slug")

must_contain = {
    "README.md": [project["site_name"], repo, site, recommended, version],
    "mkdocs.yml": [project["site_name"], project["site_tagline"], repo, site, repo_full],
    "CITATION.cff": [version, repo, site, project["artifact_title"]],
    "CITATION.bib": [version, repo],
    "codemeta.json": [version, repo, site, project["site_name"]],
    ".zenodo.json": [version, project["artifact_title"]],
    "archive/theorem-manifest.json": [version, project["upstream_commit"]],
    "docs/publication/submission-metadata.yaml": [version, project["artifact_title"]],
    "REPOSITORY_RENAME.md": [recommended],
    "docs/maintainers/rename-repository.md": [recommended],
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

readme = (ROOT / "README.md").read_text(encoding="utf-8")
for stale in (
    "Uploading this v2 tree",
    "The existing GitHub repository contains the previous PDF-based bundle",
    "paper/main.pdf",
    "paper/main.tex",
):
    if stale in readme:
        raise SystemExit(f"stale publication language in README: {stale!r}")

print("project identity audit: OK")
print(f"current repository: {repo_full}")
print(f"recommended rename: {project['repository_owner']}/{recommended}")
