#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
HTML_LINK_RE = re.compile(r"(?:href|src)=[\"']([^\"']+)[\"']")

errors: list[str] = []
files = [p for p in ROOT.rglob("*.md") if not any(x in p.parts for x in (".git", ".lake", "site", "release"))]

for source in files:
    text = source.read_text(encoding="utf-8")
    links = [m.group(1).strip() for m in LINK_RE.finditer(text)]
    links += [m.group(1).strip() for m in HTML_LINK_RE.finditer(text)]
    for raw in links:
        if raw.startswith("<") and raw.endswith(">"):
            raw = raw[1:-1]
        target = raw.split()[0].strip('"\'')
        parts = urlsplit(target)
        if parts.scheme in {"http", "https", "mailto", "data", "javascript"} or target.startswith("#"):
            continue
        path_text = unquote(parts.path)
        if not path_text:
            continue
        candidate = (source.parent / path_text).resolve()
        try:
            candidate.relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f"{source.relative_to(ROOT)}: link escapes repository: {target}")
            continue
        if candidate.is_dir():
            candidate = candidate / "index.md"
        if candidate.exists():
            continue
        # MkDocs links may omit .md and point to a page directory.
        if candidate.suffix == "" and candidate.with_suffix(".md").exists():
            continue
        errors.append(f"{source.relative_to(ROOT)}: missing target {target}")

if errors:
    raise SystemExit("Internal link audit failed:\n" + "\n".join(sorted(set(errors))))

print(f"internal link audit: OK ({len(files)} Markdown files)")
