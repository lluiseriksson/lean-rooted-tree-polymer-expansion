#!/usr/bin/env python3
from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "MANIFEST.sha256"
EXCLUDED_PARTS = {".git", ".lake", "site", "release", ".venv", ".venv-docs", "__pycache__"}

rows: list[str] = []
for path in sorted(ROOT.rglob("*"), key=lambda p: p.as_posix()):
    if not path.is_file() or path == OUT:
        continue
    rel = path.relative_to(ROOT)
    if any(part in EXCLUDED_PARTS for part in rel.parts):
        continue
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    rows.append(f"{digest}  {rel.as_posix()}")
OUT.write_text("\n".join(rows) + "\n", encoding="utf-8")
print(f"wrote {OUT.relative_to(ROOT)} with {len(rows)} entries")
