#!/usr/bin/env python3
"""Build release evidence twice and require byte-for-byte identical outputs."""
from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from project_config import ROOT, load_project, release_stem

project = load_project()
stem = release_stem(project)
release_dir = ROOT / "release"
primary = [
    f"{stem}.zip",
    f"{stem}.zip.sha256",
    f"{stem}.spdx.json",
    f"{stem}.spdx.json.sha256",
    f"{stem}.cdx.json",
    f"{stem}.cdx.json.sha256",
    f"{stem}.buildinfo.json",
    f"{stem}.buildinfo.json.sha256",
    f"{stem}.intoto.jsonl",
    f"{stem}.intoto.jsonl.sha256",
    f"{stem}.release.json",
    f"{stem}.release.json.sha256",
    f"{stem}.checksums.sha256",
]


def build() -> None:
    subprocess.run([sys.executable, "scripts/make_release.py"], cwd=ROOT, check=True)
    subprocess.run([sys.executable, "scripts/generate_sbom.py"], cwd=ROOT, check=True)
    subprocess.run([sys.executable, "scripts/generate_cyclonedx.py"], cwd=ROOT, check=True)
    subprocess.run([sys.executable, "scripts/generate_buildinfo.py"], cwd=ROOT, check=True)
    subprocess.run([sys.executable, "scripts/generate_provenance.py"], cwd=ROOT, check=True)
    subprocess.run([sys.executable, "scripts/generate_release_index.py"], cwd=ROOT, check=True)


with tempfile.TemporaryDirectory() as temp:
    first_dir = Path(temp) / "first"
    first_dir.mkdir()
    build()
    for name in primary:
        path = release_dir / name
        if not path.is_file():
            raise SystemExit(f"determinism input missing after first build: {path}")
        shutil.copy2(path, first_dir / name)
    build()
    mismatches: list[str] = []
    for name in primary:
        first = first_dir / name
        second = release_dir / name
        if first.read_bytes() != second.read_bytes():
            mismatches.append(
                f"{name}: {hashlib.sha256(first.read_bytes()).hexdigest()} != "
                f"{hashlib.sha256(second.read_bytes()).hexdigest()}"
            )
    if mismatches:
        raise SystemExit("release evidence is not deterministic:\n" + "\n".join(mismatches))

zip_hash = hashlib.sha256((release_dir / f"{stem}.zip").read_bytes()).hexdigest()
print(f"release evidence determinism: OK ({len(primary)} files)")
print(f"source ZIP sha256: {zip_hash}")
