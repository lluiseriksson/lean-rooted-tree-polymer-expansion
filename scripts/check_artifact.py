#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

required = [
    "README.md",
    "lakefile.lean",
    "lean-toolchain",
    "MarkedRootedClosure.lean",
    "MarkedRootedClosure/PaperTheorems.lean",
    "MarkedRootedClosure/Oracle.lean",
    "paper/main.tex",
    "paper/main.pdf",
    "paper/references.bib",
    "paper/graphical-abstract-final.pdf",
    "paper/graphical-abstract.png",
    "paper/cover-letter.md",
    "paper/arxiv-abstract.txt",
    "paper/submission-metadata.yaml",
    "archive/UPSTREAM.lock",
    "archive/theorem-manifest.json",
    "docs/BUILD_STATUS.md",
    "docs/SOURCE_PROVENANCE.md",
    "docs/THEOREM_MAP.md",
    "docs/NOVELTY_AND_SCOPE.md",
    "CITATION.cff",
    "codemeta.json",
]
missing = [p for p in required if not (ROOT / p).is_file()]
if missing:
    raise SystemExit("Missing required artifact files: " + ", ".join(missing))

manifest = json.loads((ROOT / "archive/theorem-manifest.json").read_text(encoding="utf-8"))
endpoints = manifest.get("endpoints", [])
if len(endpoints) != 3:
    raise SystemExit("Theorem manifest must expose exactly three publication endpoints")

public_names = {e["public_name"] for e in endpoints}
expected_names = {
    "normalizedRootedChildFactorialTreeBound",
    "markedRootLeafGeometricBound",
    "targetPreservingWeightedTreeBound",
}
if public_names != expected_names:
    raise SystemExit(f"Unexpected theorem endpoint set: {sorted(public_names)}")

wrapper = (ROOT / "MarkedRootedClosure/PaperTheorems.lean").read_text(encoding="utf-8")
for name in expected_names:
    if not re.search(rf"\btheorem\s+{re.escape(name)}\b", wrapper):
        raise SystemExit(f"Public theorem missing from wrapper: {name}")

lock_text = (ROOT / "archive/UPSTREAM.lock").read_text(encoding="utf-8")
commit = manifest["upstream"]["commit"]
if f"UPSTREAM_COMMIT={commit}" not in lock_text:
    raise SystemExit("Upstream commit differs between lock and JSON manifest")
if commit not in (ROOT / "lakefile.lean").read_text(encoding="utf-8"):
    raise SystemExit("Pinned upstream commit is missing from lakefile.lean")

for name in ("CITATION.cff", "codemeta.json"):
    text = (ROOT / name).read_text(encoding="utf-8")
    if "Marked Rooted-Tree" not in text:
        raise SystemExit(f"Publication title missing from {name}")

for rel in ("paper/main.pdf", "paper/graphical-abstract-final.pdf"):
    pdf = ROOT / rel
    if pdf.stat().st_size < 50_000:
        raise SystemExit(f"PDF is unexpectedly small: {rel}")
    if not pdf.read_bytes().startswith(b"%PDF-"):
        raise SystemExit(f"Not a PDF file: {rel}")

main_pdf = ROOT / "paper/main.pdf"
sha = hashlib.sha256(main_pdf.read_bytes()).hexdigest()
print("artifact audit: OK")
print(f"paper pages expected: 16")
print(f"paper sha256: {sha}")
print(f"upstream commit: {commit}")
