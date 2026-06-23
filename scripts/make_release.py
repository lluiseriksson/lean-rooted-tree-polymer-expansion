#!/usr/bin/env python3
from __future__ import annotations

import shutil
import stat
import zipfile
from datetime import date
from pathlib import Path

from project_config import ROOT, load_project, release_stem
from release_inventory import sha256, write_sidecar
from source_inventory import MANIFEST_REL, collect_source_files, render_manifest

project = load_project()
name = release_stem(project)
out = ROOT / "release"
zip_path = out / f"{name}.zip"
release_date = date.fromisoformat(project["release_date"])
fixed_time = (release_date.year, release_date.month, release_date.day, 12, 0, 0)


shutil.rmtree(out, ignore_errors=True)
out.mkdir(parents=True)

source_files = collect_source_files(ROOT, include_manifest=False)
manifest_bytes = render_manifest(ROOT, source_files)
(ROOT / MANIFEST_REL).write_bytes(manifest_bytes)
files = sorted(
    [*source_files, ROOT / MANIFEST_REL],
    key=lambda path: path.relative_to(ROOT).as_posix(),
)

required = {
    Path("project.json"),
    MANIFEST_REL,
    Path("lake-manifest.json"),
    Path("docs/paper/manifest.json"),
    Path("archive/theorem-manifest.json"),
    Path("MarkedRootedClosure/PaperTheorems.lean"),
}
found = {path.relative_to(ROOT) for path in files}
missing = required - found
if missing:
    raise SystemExit("release input missing required files: " + ", ".join(map(str, sorted(missing))))

with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        data = manifest_bytes if rel == MANIFEST_REL.as_posix() else path.read_bytes()
        info = zipfile.ZipInfo(f"{name}/{rel}", fixed_time)
        info.compress_type = zipfile.ZIP_DEFLATED
        mode = 0o755 if path.stat().st_mode & stat.S_IXUSR else 0o644
        info.external_attr = (mode & 0xFFFF) << 16
        info.create_system = 3
        zf.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

digest = sha256(zip_path)
write_sidecar(zip_path)
print(f"release created: {zip_path}")
print(f"sha256: {digest}")
