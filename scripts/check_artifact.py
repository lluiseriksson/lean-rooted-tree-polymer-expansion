#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

from project_config import ROOT, load_project

project = load_project()
version = project["version"]
upstream = project["upstream_commit"]

required = [
    "README.md",
    "project.json",
    "REPOSITORY_RENAME.md",
    "AGENTS.md",
    "GOVERNANCE.md",
    "SUPPORT.md",
    "MIGRATION.md",
    "LICENSE",
    "NOTICE",
    "CITATION.cff",
    "CITATION.bib",
    "codemeta.json",
    ".zenodo.json",
    "lakefile.lean",
    "lake-manifest.json",
    "lean-toolchain",
    "MarkedRootedClosure.lean",
    "MarkedRootedClosure/PaperTheorems.lean",
    "MarkedRootedClosure/Oracle.lean",
    "mkdocs.yml",
    "requirements-docs.txt",
    "docs/index.md",
    "docs/about/overview.md",
    "docs/about/claims.md",
    "docs/about/notation.md",
    "docs/formalization/index.md",
    "docs/paper/index.md",
    "docs/paper/manifest.json",
    "docs/paper/00-reader-guide.md",
    "docs/paper/01-introduction.md",
    "docs/paper/07-target-preserving-decay.md",
    "docs/paper/11-limitations.md",
    "docs/paper/references.md",
    "docs/paper/references.bib",
    "docs/publication/author-declarations.md",
    "docs/publication/submission-metadata.md",
    "docs/publication/submission-metadata.yaml",
    "docs/assets/source/graphical-abstract.tex",
    "docs/assets/stylesheets/print.css",
    "docs/artifact/theorem-map.md",
    "docs/artifact/source-provenance.md",
    "docs/artifact/reproducibility.md",
    "docs/maintainers/rename-repository.md",
    "docs/maintainers/release-playbook.md",
    "docs/assets/images/proof-pipeline.png",
    "archive/UPSTREAM.lock",
    "archive/theorem-manifest.json",
    ".github/workflows/ci.yml",
    ".github/workflows/pages.yml",
    ".github/workflows/release.yml",
    ".github/workflows/dependency-review.yml",
    "scripts/assemble_paper.py",
    "scripts/check_paper_manifest.py",
    "scripts/check_lake_lock.py",
    "scripts/check_project_identity.py",
    "scripts/rename_repository.py",
    "scripts/generate_sbom.py",
    "scripts/check_release_determinism.py",
    "scripts/verify_release.py",
]
missing = [p for p in required if not (ROOT / p).is_file()]
if missing:
    raise SystemExit("Missing required files: " + ", ".join(missing))

for forbidden in (ROOT / "paper", ROOT / "release-artifacts"):
    if forbidden.exists():
        raise SystemExit(f"Legacy standalone-paper path must be removed: {forbidden.name}")

for path in ROOT.rglob("*"):
    if not path.is_file():
        continue
    rel = path.relative_to(ROOT)
    if rel.parts and rel.parts[0] in {
        "release", ".lake", "site", ".git", ".venv", ".venv-docs"
    }:
        continue
    if rel.parts[:2] == ("docs", "generated"):
        continue
    if path.suffix.lower() in {".pdf", ".zip"}:
        raise SystemExit(f"Tracked standalone binary is forbidden: {rel}")

manifest = json.loads((ROOT / "archive/theorem-manifest.json").read_text())
if manifest.get("version") != version:
    raise SystemExit("Theorem manifest version mismatch")
if manifest.get("publication_model") != project["publication_model"]:
    raise SystemExit("Publication model mismatch")
if manifest["upstream"]["commit"] != upstream:
    raise SystemExit("Unexpected upstream commit in theorem manifest")

endpoints = manifest.get("endpoints", [])
expected_names = {
    "normalizedRootedChildFactorialTreeBound",
    "markedRootLeafGeometricBound",
    "targetPreservingWeightedTreeBound",
}
if {e.get("public_name") for e in endpoints} != expected_names:
    raise SystemExit("Unexpected publication endpoint set")

wrapper = (ROOT / "MarkedRootedClosure/PaperTheorems.lean").read_text()
for name in expected_names:
    if not re.search(rf"\btheorem\s+{re.escape(name)}\b", wrapper):
        raise SystemExit(f"Public theorem missing from wrapper: {name}")

json_files = [
    "project.json",
    "lake-manifest.json",
    "archive/theorem-manifest.json",
    "docs/paper/manifest.json",
    "codemeta.json",
    ".zenodo.json",
]
for rel in json_files:
    json.loads((ROOT / rel).read_text())

for rel in (
    "CITATION.cff",
    "CITATION.bib",
    "codemeta.json",
    ".zenodo.json",
    "CHANGELOG.md",
    "RELEASE_NOTES.md",
):
    text = (ROOT / rel).read_text()
    if version not in text:
        raise SystemExit(f"Version {version} missing from {rel}")

all_text: list[tuple[Path, str]] = []
for path in ROOT.rglob("*"):
    if not path.is_file() or path.suffix.lower() in {".png", ".jpg", ".jpeg"}:
        continue
    if path.resolve() == Path(__file__).resolve():
        continue
    rel = path.relative_to(ROOT)
    if rel in {Path("scripts/check_artifact.py"), Path("scripts/check_project_identity.py")} :
        continue
    if any(part in {".git", ".lake", "site", "release", ".venv", ".venv-docs"}
           for part in rel.parts):
        continue
    try:
        text = path.read_text()
    except UnicodeDecodeError:
        continue
    all_text.append((path, text))

for path, text in all_text:
    rel = path.relative_to(ROOT)
    for stale in (
        "paper/main.pdf",
        "paper/main.tex",
        "release-artifacts/",
        "Uploading this v2 tree",
    ):
        if stale in text:
            raise SystemExit(f"Stale standalone-publication reference {stale!r} in {rel}")

makefile = (ROOT / "Makefile").read_text()
lean_block = makefile.split("lean:", 1)[1].split("\n\n", 1)[0]
if "lake update" in lean_block:
    raise SystemExit("ordinary Lean verification must not refresh dependency locks")
if "lock-refresh:" not in makefile or "lake update" not in makefile.split("lock-refresh:", 1)[1]:
    raise SystemExit("explicit lock-refresh target is missing")

full = ROOT / "docs/generated/full-article.md"
if full.exists():
    text = full.read_text(encoding="utf-8")
    if not text.startswith("<!-- GENERATED FILE:"):
        raise SystemExit("generated full article lacks its do-not-edit marker")

png = ROOT / "docs/assets/images/proof-pipeline.png"
if png.stat().st_size < 20_000 or not png.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"):
    raise SystemExit("Graphical abstract is missing or invalid")

print("artifact audit: OK")
print(f"version: {version}")
print(f"publication endpoints: {len(endpoints)}")
print(f"upstream commit: {upstream}")
print("paper model: canonical sections + generated continuous HTML view")
