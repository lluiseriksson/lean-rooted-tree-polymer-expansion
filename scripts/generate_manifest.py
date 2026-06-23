#!/usr/bin/env python3
from __future__ import annotations

import hashlib
from pathlib import Path

from project_config import ROOT

OUT = ROOT / "MANIFEST.sha256"
EXCLUDED_PARTS = {
    ".git", ".lake", "site", "release", ".venv", ".venv-docs",
    "__pycache__", "docs/generated",
}


def excluded(rel: Path) -> bool:
    value = rel.as_posix()
    return (
        any(value == item or value.startswith(item + "/") for item in EXCLUDED_PARTS)
        or any(part in {"__pycache__", ".pytest_cache", ".mypy_cache"} for part in rel.parts)
    )

rows: list[str] = []
for path in sorted(ROOT.rglob("*"), key=lambda p: p.as_posix()):
    if not path.is_file() or path == OUT:
        continue
    rel = path.relative_to(ROOT)
    if excluded(rel):
        continue
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    rows.append(f"{digest}  {rel.as_posix()}")
OUT.write_bytes(("\n".join(rows) + "\n").encode("utf-8"))
print(f"wrote {OUT.relative_to(ROOT)} with {len(rows)} entries")
