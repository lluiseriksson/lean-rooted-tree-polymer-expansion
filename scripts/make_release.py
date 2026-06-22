#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import shutil
import stat
import zipfile
from datetime import date
from pathlib import Path

from project_config import ROOT, load_project, release_stem

project = load_project()
name = release_stem(project)
out = ROOT / "release"
zip_path = out / f"{name}.zip"
sidecar = out / f"{name}.zip.sha256"
excluded_roots = {
    ".git", ".lake", "site", "release", ".venv", ".venv-docs",
    "__pycache__", "docs/generated",
}
release_date = date.fromisoformat(project["release_date"])
fixed_time = (release_date.year, release_date.month, release_date.day, 12, 0, 0)


def is_excluded(rel: Path) -> bool:
    value = rel.as_posix()
    return (
        any(value == item or value.startswith(item + "/") for item in excluded_roots)
        or any(part in {"__pycache__", ".pytest_cache", ".mypy_cache"} for part in rel.parts)
    )


shutil.rmtree(out, ignore_errors=True)
out.mkdir(parents=True)

files: list[Path] = []
for path in sorted(ROOT.rglob("*"), key=lambda p: p.as_posix()):
    if not path.is_file():
        continue
    rel = path.relative_to(ROOT)
    if is_excluded(rel):
        continue
    files.append(path)

required = {
    Path("project.json"),
    Path("lake-manifest.json"),
    Path("docs/paper/manifest.json"),
    Path("archive/theorem-manifest.json"),
    Path("MarkedRootedClosure/PaperTheorems.lean"),
}
found = {path.relative_to(ROOT) for path in files}
missing = required - found
if missing:
    raise SystemExit("release input missing required files: " + ", ".join(map(str, sorted(missing))))

manifest_rows = []
for path in files:
    if path.name == "MANIFEST.sha256":
        continue
    rel = path.relative_to(ROOT).as_posix()
    manifest_rows.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {rel}")
manifest_bytes = ("\n".join(manifest_rows) + "\n").encode("utf-8")

with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        data = manifest_bytes if rel == "MANIFEST.sha256" else path.read_bytes()
        info = zipfile.ZipInfo(f"{name}/{rel}", fixed_time)
        info.compress_type = zipfile.ZIP_DEFLATED
        mode = 0o755 if path.stat().st_mode & stat.S_IXUSR else 0o644
        info.external_attr = (mode & 0xFFFF) << 16
        info.create_system = 3
        zf.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

digest = hashlib.sha256(zip_path.read_bytes()).hexdigest()
sidecar.write_text(f"{digest}  {zip_path.name}\n", encoding="utf-8")
print(f"release created: {zip_path}")
print(f"sha256: {digest}")
