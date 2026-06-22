#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from project_config import ROOT

PAPER = ROOT / "docs" / "paper"
manifest = json.loads((PAPER / "manifest.json").read_text(encoding="utf-8"))
sections = manifest.get("sections")
if not isinstance(sections, list) or not sections:
    raise SystemExit("paper manifest must contain a nonempty 'sections' list")
if len(sections) != len(set(sections)):
    raise SystemExit("paper manifest contains duplicate section paths")

missing = [name for name in sections if not (PAPER / name).is_file()]
if missing:
    raise SystemExit("paper manifest has missing files: " + ", ".join(missing))

canonical = {
    p.name
    for p in PAPER.glob("*.md")
    if p.name != "index.md" and not p.name.startswith("draft-")
}
unlisted = sorted(canonical - set(sections))
if unlisted:
    raise SystemExit("canonical paper pages absent from manifest: " + ", ".join(unlisted))

for name in sections:
    text = (PAPER / name).read_text(encoding="utf-8")
    first = next((line for line in text.splitlines() if line.strip()), "")
    if not first.startswith("# "):
        raise SystemExit(f"paper section must start with one H1 heading: {name}")

print(f"paper manifest audit: OK ({len(sections)} canonical sections)")
