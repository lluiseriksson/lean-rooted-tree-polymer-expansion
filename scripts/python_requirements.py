#!/usr/bin/env python3
"""Utilities for exact Python requirement files used by repository tooling."""
from __future__ import annotations

import re
from pathlib import Path

REQUIREMENT_RE = re.compile(r"([A-Za-z0-9_.-]+)==([^\s#]+)")


def canonical_name(name: str) -> str:
    """Return the PEP 503 canonical package name."""
    return re.sub(r"[-_.]+", "-", name).lower()


def parse_exact_requirements(path: Path) -> list[tuple[str, str]]:
    """Parse a comments-only, exact ``name==version`` requirements file."""
    result: list[tuple[str, str]] = []
    seen: set[str] = set()
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        match = REQUIREMENT_RE.fullmatch(line)
        if not match:
            raise ValueError(f"{path}:{lineno}: expected exact name==version pin: {line!r}")
        name, version = match.groups()
        canonical = canonical_name(name)
        if canonical in seen:
            raise ValueError(f"{path}:{lineno}: duplicate canonical package name: {name}")
        seen.add(canonical)
        result.append((name, version))
    if not result:
        raise ValueError(f"empty requirements file: {path}")
    return result


def requirement_map(path: Path) -> dict[str, tuple[str, str]]:
    """Map canonical names to their display names and versions."""
    return {canonical_name(name): (name, version) for name, version in parse_exact_requirements(path)}
