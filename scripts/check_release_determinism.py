#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import shutil
import subprocess
import tempfile
from pathlib import Path

from project_config import ROOT, load_project, release_stem

project = load_project()
stem = release_stem(project)
zip_path = ROOT / "release" / f"{stem}.zip"

with tempfile.TemporaryDirectory() as temp:
    first = Path(temp) / "first.zip"
    subprocess.run(["python3", "scripts/make_release.py"], cwd=ROOT, check=True)
    shutil.copy2(zip_path, first)
    first_hash = hashlib.sha256(first.read_bytes()).hexdigest()
    subprocess.run(["python3", "scripts/make_release.py"], cwd=ROOT, check=True)
    second_hash = hashlib.sha256(zip_path.read_bytes()).hexdigest()
    if first_hash != second_hash or first.read_bytes() != zip_path.read_bytes():
        raise SystemExit(
            f"release is not deterministic: first={first_hash}, second={second_hash}"
        )
print(f"release determinism: OK ({first_hash})")
