#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

for rel in ("codemeta.json", ".zenodo.json", "archive/theorem-manifest.json"):
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
    ):
        with (ROOT / rel).open(encoding="utf-8") as handle:
            yaml.safe_load(handle)
    print("metadata audit: JSON and YAML parse successfully")

cffconvert = shutil.which("cffconvert")
if cffconvert:
    subprocess.run([cffconvert, "--validate"], cwd=ROOT, check=True)
else:
    print("metadata audit: cffconvert unavailable; schema validation deferred")
