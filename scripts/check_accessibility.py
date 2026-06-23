#!/usr/bin/env python3
"""Dependency-free accessibility checks for Markdown documentation."""
from __future__ import annotations

import re
from pathlib import Path

from project_config import ROOT

HEADING_RE = re.compile(r"^(#{1,6})\s+\S")
IMAGE_RE = re.compile(r"!\[([^\]]*)\]\([^\)]+\)")
RAW_IMAGE_RE = re.compile(r"<img\b([^>]*)>", re.IGNORECASE)
LINK_TEXT_RE = re.compile(r"\[([^\]]+)\]\([^\)]+\)")


def _visible_lines(text: str) -> list[tuple[int, str]]:
    lines: list[tuple[int, str]] = []
    fence: str | None = None
    in_comment = False
    for lineno, raw in enumerate(text.splitlines(), 1):
        line = raw
        if in_comment:
            if "-->" in line:
                line = line.split("-->", 1)[1]
                in_comment = False
            else:
                continue
        if "<!--" in line:
            before, after = line.split("<!--", 1)
            line = before
            if "-->" not in after:
                in_comment = True
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            marker = stripped[:3]
            if fence is None:
                fence = marker
            elif marker == fence:
                fence = None
            continue
        if fence is None:
            lines.append((lineno, line))
    return lines


def validate_file(path: Path) -> list[str]:
    errors: list[str] = []
    visible = _visible_lines(path.read_text(encoding="utf-8"))
    levels: list[tuple[int, int]] = []
    for lineno, line in visible:
        match = HEADING_RE.match(line)
        if match:
            levels.append((lineno, len(match.group(1))))
        for alt in IMAGE_RE.findall(line):
            if not alt.strip():
                errors.append(f"{path}:{lineno}: Markdown image has empty alt text")
        for attrs in RAW_IMAGE_RE.findall(line):
            if not re.search(r"\balt\s*=\s*(['\"]).*?\1", attrs, re.IGNORECASE):
                errors.append(f"{path}:{lineno}: raw HTML image lacks alt attribute")
        for text in LINK_TEXT_RE.findall(line):
            if text.strip().casefold() in {"here", "click here", "this link"}:
                errors.append(f"{path}:{lineno}: non-descriptive link text {text!r}")
    if levels:
        first_line, first_level = levels[0]
        if first_level != 1:
            errors.append(f"{path}:{first_line}: first heading must be level 1")
        previous = first_level
        for lineno, level in levels[1:]:
            if level > previous + 1:
                errors.append(
                    f"{path}:{lineno}: heading level jumps from H{previous} to H{level}"
                )
            previous = level
    return errors


def validate(root: Path = ROOT) -> list[str]:
    paths = [root / "README.md"]
    paths.extend(
        path
        for path in sorted((root / "docs").rglob("*.md"))
        if "generated" not in path.parts
    )
    errors: list[str] = []
    for path in paths:
        errors.extend(validate_file(path))
    mkdocs = (root / "mkdocs.yml").read_text(encoding="utf-8")
    if "language: en" not in mkdocs:
        errors.append("mkdocs.yml must declare the site language")
    return errors


def main() -> None:
    errors = validate()
    if errors:
        raise SystemExit("Accessibility audit failed:\n" + "\n".join(f"- {e}" for e in errors))
    count = 1 + len([p for p in (ROOT / "docs").rglob("*.md") if "generated" not in p.parts])
    print(f"accessibility audit: OK ({count} Markdown files)")


if __name__ == "__main__":
    main()
