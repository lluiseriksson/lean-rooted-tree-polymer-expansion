#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

from project_config import ROOT, load_project

project = load_project()
for rel in (
    "project.json",
    "lake-manifest.json",
    "codemeta.json",
    ".zenodo.json",
    "archive/theorem-manifest.json",
    "docs/paper/manifest.json",
):
    json.loads((ROOT / rel).read_text(encoding="utf-8"))

try:
    import yaml  # type: ignore
except ImportError:
    print("metadata audit: PyYAML unavailable; JSON checks completed")
else:
    for rel in (
        "CITATION.cff",
        "mkdocs.yml",
        "docs/publication/submission-metadata.yaml",
        ".github/dependabot.yml",
        ".github/workflows/ci.yml",
        ".github/workflows/pages.yml",
        ".github/workflows/release.yml",
        ".github/workflows/dependency-review.yml",
    ):
        with (ROOT / rel).open(encoding="utf-8") as handle:
            value = yaml.safe_load(handle)
            if value is None:
                raise SystemExit(f"empty YAML document: {rel}")
    print("metadata audit: JSON and YAML parse successfully")

cff_text = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
for needle in (
    "cff-version: 1.2.0",
    f"version: {project['version']}",
    project["artifact_title"],
):
    if needle not in cff_text:
        raise SystemExit(f"CITATION.cff missing {needle!r}")

cffconvert = shutil.which("cffconvert")
if cffconvert:
    subprocess.run([cffconvert, "--validate"], cwd=ROOT, check=True)
else:
    print("metadata audit: cffconvert unavailable; schema validation deferred to CI")
