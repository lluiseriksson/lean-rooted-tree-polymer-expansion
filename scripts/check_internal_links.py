#!/usr/bin/env python3
from __future__ import annotations

import html
import re
import unicodedata
from pathlib import Path
from urllib.parse import unquote, urlsplit

from project_config import ROOT
from source_inventory import collect_source_files

LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
HTML_LINK_RE = re.compile(r"(?:href|src)=[\"']([^\"']+)[\"']")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
EXPLICIT_ID_RE = re.compile(r"\s*\{#([A-Za-z0-9_.:-]+)\}\s*$")


def slugify_heading(value: str) -> str:
    value = EXPLICIT_ID_RE.sub("", value)
    value = re.sub(r"<[^>]+>", "", value)
    value = re.sub(r"`([^`]*)`", r"\1", value)
    value = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", value)
    value = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", value)
    value = re.sub(r"[*_~]", "", value)
    value = html.unescape(value)
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    value = value.lower()
    value = re.sub(r"[^a-z0-9 _-]", "", value)
    value = re.sub(r"[ _-]+", "-", value).strip("-")
    return value


def anchors_for(path: Path) -> set[str]:
    if path.suffix.lower() != ".md":
        return set()
    anchors: set[str] = set()
    counts: dict[str, int] = {}
    in_fence = False
    fence = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            marker = stripped[:3]
            if not in_fence:
                in_fence = True
                fence = marker
            elif marker == fence:
                in_fence = False
                fence = ""
            continue
        if in_fence:
            continue
        match = HEADING_RE.match(line)
        if not match:
            continue
        title = match.group(2)
        explicit = EXPLICIT_ID_RE.search(title)
        if explicit:
            anchors.add(explicit.group(1))
            continue
        base = slugify_heading(title)
        if not base:
            continue
        count = counts.get(base, 0)
        anchors.add(base if count == 0 else f"{base}_{count}")
        counts[base] = count + 1
    return anchors


errors: list[str] = []
files = [path for path in collect_source_files(ROOT) if path.suffix.lower() == ".md"]
generated = ROOT / "docs" / "generated" / "full-article.md"
if generated.is_file():
    files.append(generated)
files.sort(key=lambda path: path.relative_to(ROOT).as_posix())
anchor_cache: dict[Path, set[str]] = {}

for source in files:
    text = source.read_text(encoding="utf-8")
    links = [m.group(1).strip() for m in LINK_RE.finditer(text)]
    links += [m.group(1).strip() for m in HTML_LINK_RE.finditer(text)]
    for raw in links:
        if raw.startswith("<") and raw.endswith(">"):
            raw = raw[1:-1]
        target = raw.split()[0].strip("\"'")
        parts = urlsplit(target)
        if parts.scheme in {"http", "https", "mailto", "tel", "data", "javascript"}:
            continue
        path_text = unquote(parts.path)
        if not path_text:
            candidate = source
        elif path_text.startswith("/"):
            # Site-root links are resolved relative to docs/ for MkDocs.
            candidate = (ROOT / "docs" / path_text.lstrip("/")).resolve()
        else:
            candidate = (source.parent / path_text).resolve()
        try:
            candidate.relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f"{source.relative_to(ROOT)}: link escapes repository: {target}")
            continue
        if candidate.is_dir():
            candidate = candidate / "index.md"
        if not candidate.exists() and candidate.suffix == "":
            if candidate.with_suffix(".md").exists():
                candidate = candidate.with_suffix(".md")
        if not candidate.exists():
            errors.append(f"{source.relative_to(ROOT)}: missing target {target}")
            continue
        if parts.fragment and candidate.suffix.lower() == ".md":
            anchors = anchor_cache.setdefault(candidate, anchors_for(candidate))
            fragment = unquote(parts.fragment)
            if fragment not in anchors:
                errors.append(
                    f"{source.relative_to(ROOT)}: missing anchor #{fragment} in "
                    f"{candidate.relative_to(ROOT)}"
                )

if errors:
    raise SystemExit("Internal link audit failed:\n" + "\n".join(sorted(set(errors))))

print(f"internal link audit: OK ({len(files)} Markdown files, local anchors checked)")
