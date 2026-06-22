#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

from project_config import ROOT, load_project

project = load_project()
manifest = json.loads((ROOT / "lake-manifest.json").read_text(encoding="utf-8"))
packages = {pkg["name"]: pkg for pkg in manifest.get("packages", [])}

for name in ("YangMills", "mathlib"):
    if name not in packages:
        raise SystemExit(f"lake-manifest.json does not contain package {name}")

checks = {
    "YangMills": project["upstream_commit"],
    "mathlib": project["mathlib_commit"],
}
for name, expected in checks.items():
    package = packages[name]
    for field in ("rev", "inputRev"):
        if package.get(field) != expected:
            raise SystemExit(
                f"{name}.{field} mismatch: expected {expected}, got {package.get(field)}"
            )

lock_text = (ROOT / "archive" / "UPSTREAM.lock").read_text(encoding="utf-8")
expected_lock = {
    "UPSTREAM_COMMIT": project["upstream_commit"],
    "LEAN_TOOLCHAIN": project["lean_toolchain"],
    "MATHLIB_COMMIT": project["mathlib_commit"],
}
for key, value in expected_lock.items():
    if f"{key}={value}" not in lock_text:
        raise SystemExit(f"archive/UPSTREAM.lock mismatch for {key}")

lakefile = (ROOT / "lakefile.lean").read_text(encoding="utf-8")
if project["upstream_commit"] not in lakefile:
    raise SystemExit("lakefile.lean does not contain the pinned upstream commit")
if not re.search(rf'version\s*:=\s*v!"{re.escape(project["version"])}"', lakefile):
    raise SystemExit("lakefile.lean package version differs from project.json")

toolchain = (ROOT / "lean-toolchain").read_text(encoding="utf-8").strip()
if toolchain != project["lean_toolchain"]:
    raise SystemExit("lean-toolchain differs from project.json")

print("Lake lock audit: OK")
print(f"upstream: {project['upstream_commit']}")
print(f"mathlib: {project['mathlib_commit']}")
print(f"toolchain: {project['lean_toolchain']}")
