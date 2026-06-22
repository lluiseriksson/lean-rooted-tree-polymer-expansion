#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import shutil
import stat
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = json.loads((ROOT / "archive/theorem-manifest.json").read_text())["version"]
NAME = f"marked-rooted-closure-v{VERSION}"
OUT = ROOT / "release"
ZIP = OUT / f"{NAME}.zip"
SIDE = OUT / f"{NAME}.zip.sha256"
EXCLUDED = {".git", ".lake", "site", "release", ".venv", ".venv-docs", "__pycache__"}
FIXED_TIME = (2026, 6, 22, 12, 0, 0)

shutil.rmtree(OUT, ignore_errors=True)
OUT.mkdir(parents=True)

files: list[Path] = []
for path in sorted(ROOT.rglob("*"), key=lambda p: p.as_posix()):
    if not path.is_file():
        continue
    rel = path.relative_to(ROOT)
    if any(part in EXCLUDED for part in rel.parts):
        continue
    files.append(path)

# Create an archive-local manifest from the exact bytes to be written.
manifest_rows = []
for path in files:
    if path.name == "MANIFEST.sha256":
        continue
    rel = path.relative_to(ROOT).as_posix()
    manifest_rows.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {rel}")
manifest_bytes = ("\n".join(manifest_rows) + "\n").encode()

with zipfile.ZipFile(ZIP, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        data = manifest_bytes if rel == "MANIFEST.sha256" else path.read_bytes()
        zi = zipfile.ZipInfo(f"{NAME}/{rel}", FIXED_TIME)
        zi.compress_type = zipfile.ZIP_DEFLATED
        mode = 0o755 if path.stat().st_mode & stat.S_IXUSR else 0o644
        zi.external_attr = (mode & 0xFFFF) << 16
        zi.create_system = 3
        zf.writestr(zi, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

digest = hashlib.sha256(ZIP.read_bytes()).hexdigest()
SIDE.write_text(f"{digest}  {ZIP.name}\n")
print(f"release created: {ZIP}")
print(f"sha256: {digest}")
