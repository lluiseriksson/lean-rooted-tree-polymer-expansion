#!/usr/bin/env python3
"""Build release evidence twice and require byte-for-byte identical outputs."""
from __future__ import annotations

import hashlib
import shutil
import sys
import tempfile
from pathlib import Path

from project_config import ROOT, load_project, release_stem
from release_inventory import expected_release_names, verify_release_inventory
from process_runner import run_checked

project = load_project()
stem = release_stem(project)
release_dir = ROOT / "release"
primary = list(expected_release_names(project))


def build() -> None:
    for relative in (
        "scripts/make_release.py",
        "scripts/generate_sbom.py",
        "scripts/generate_cyclonedx.py",
        "scripts/generate_buildinfo.py",
        "scripts/generate_provenance.py",
        "scripts/generate_release_index.py",
    ):
        run_checked([sys.executable, relative], cwd=ROOT, timeout=180)
    verify_release_inventory(project, release_dir)


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
