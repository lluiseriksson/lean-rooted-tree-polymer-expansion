#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "2.0.0"
CURRENT_UPSTREAM = "4e45246aa109671d25fcd01ba1abf7bc3f8506d1"
OLD_UPSTREAM = "83d18a113e3fa22ada23b13361fb84015a1c80ed"

required = [
    "README.md",
    "AGENTS.md",
    "MIGRATION.md",
    "LICENSE",
    "NOTICE",
    "CITATION.cff",
    "CITATION.bib",
    "codemeta.json",
    ".zenodo.json",
    "lakefile.lean",
    "lean-toolchain",
    "MarkedRootedClosure.lean",
    "MarkedRootedClosure/PaperTheorems.lean",
    "MarkedRootedClosure/Oracle.lean",
    "mkdocs.yml",
    "requirements-docs.txt",
    "docs/index.md",
    "docs/paper/index.md",
    "docs/paper/01-introduction.md",
    "docs/paper/07-target-preserving-decay.md",
    "docs/paper/11-limitations.md",
    "docs/paper/references.md",
    "docs/paper/references.bib",
    "docs/publication/author-declarations.md",
    "docs/publication/submission-metadata.md",
    "docs/publication/submission-metadata.yaml",
    "docs/assets/source/graphical-abstract.tex",
    "docs/artifact/theorem-map.md",
    "docs/artifact/source-provenance.md",
    "docs/artifact/reproducibility.md",
    "docs/maintainers/upload-and-migration.md",
    "docs/assets/images/proof-pipeline.png",
    "archive/UPSTREAM.lock",
    "archive/theorem-manifest.json",
    ".github/workflows/ci.yml",
    ".github/workflows/pages.yml",
    ".github/workflows/release.yml",
    ".github/workflows/dependency-review.yml",
    "scripts/verify_release.py",
    "docs/artifact/supply-chain.md",
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
    if rel.parts and rel.parts[0] in {"release", ".lake", "site", ".git"}:
        continue
    if path.suffix.lower() in {".pdf", ".zip"}:
        raise SystemExit(f"Tracked standalone binary is forbidden in v2: {rel}")

manifest = json.loads((ROOT / "archive/theorem-manifest.json").read_text())
if manifest.get("version") != VERSION:
    raise SystemExit("Theorem manifest version mismatch")
if manifest.get("publication_model") != "integrated-documentation":
    raise SystemExit("Publication model must be integrated-documentation")
if manifest["upstream"]["commit"] != CURRENT_UPSTREAM:
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

lock = (ROOT / "archive/UPSTREAM.lock").read_text()
lakefile = (ROOT / "lakefile.lean").read_text()
toolchain = (ROOT / "lean-toolchain").read_text().strip()
if f"UPSTREAM_COMMIT={CURRENT_UPSTREAM}" not in lock:
    raise SystemExit("Upstream lock does not contain current commit")
if CURRENT_UPSTREAM not in lakefile:
    raise SystemExit("Lakefile does not contain current upstream commit")
if f"LEAN_TOOLCHAIN={toolchain}" not in lock:
    raise SystemExit("Lean toolchain differs between lock and lean-toolchain")

json_files = ["archive/theorem-manifest.json", "codemeta.json", ".zenodo.json"]
for rel in json_files:
    json.loads((ROOT / rel).read_text())

for rel in ("CITATION.cff", "codemeta.json", ".zenodo.json", "CHANGELOG.md"):
    text = (ROOT / rel).read_text()
    if VERSION not in text:
        raise SystemExit(f"Version {VERSION} missing from {rel}")

all_text: list[tuple[Path, str]] = []
for path in ROOT.rglob("*"):
    if not path.is_file() or path.suffix.lower() in {".png", ".jpg", ".jpeg"}:
        continue
    if path.resolve() == Path(__file__).resolve():
        continue
    if any(part in {".git", ".lake", "site", "release"} for part in path.parts):
        continue
    try:
        text = path.read_text()
    except UnicodeDecodeError:
        continue
    all_text.append((path, text))

for path, text in all_text:
    rel = path.relative_to(ROOT)
    if OLD_UPSTREAM in text:
        raise SystemExit(f"Stale upstream commit in {rel}")
    for stale in ("paper/main.pdf", "make paper", "paper/main.tex"):
        if stale in text:
            raise SystemExit(f"Stale standalone-paper reference {stale!r} in {rel}")

readme = (ROOT / "README.md").read_text()
if "docs/paper/index.md" not in readme or "no separately tracked manuscript PDF" not in readme:
    raise SystemExit("README does not explain the integrated-paper model")

png = ROOT / "docs/assets/images/proof-pipeline.png"
if png.stat().st_size < 20_000 or not png.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"):
    raise SystemExit("Graphical abstract is missing or invalid")

print("artifact audit: OK")
print(f"version: {VERSION}")
print(f"publication endpoints: {len(endpoints)}")
print(f"upstream commit: {CURRENT_UPSTREAM}")
print("paper model: integrated MkDocs documentation")
