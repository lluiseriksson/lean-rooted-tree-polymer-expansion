#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import sys
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "release"

if len(sys.argv) > 1:
    zip_path = Path(sys.argv[1]).resolve()
else:
    candidates = sorted(RELEASE.glob("marked-rooted-closure-v*.zip"))
    if not candidates:
        raise SystemExit("No release ZIP found")
    zip_path = candidates[-1]

sidecar = zip_path.with_suffix(zip_path.suffix + ".sha256")
if not sidecar.is_file():
    raise SystemExit(f"Missing SHA-256 sidecar: {sidecar}")
expected = sidecar.read_text(encoding="utf-8").split()[0]
actual = hashlib.sha256(zip_path.read_bytes()).hexdigest()
if expected != actual:
    raise SystemExit(f"ZIP digest mismatch: expected {expected}, got {actual}")

with zipfile.ZipFile(zip_path) as zf:
    bad = zf.testzip()
    if bad:
        raise SystemExit(f"Corrupt ZIP member: {bad}")
    names = [PurePosixPath(info.filename) for info in zf.infolist() if not info.is_dir()]
    roots = {name.parts[0] for name in names if name.parts}
    if len(roots) != 1:
        raise SystemExit(f"Archive must have exactly one root directory, found: {roots}")
    root = next(iter(roots))
    rel_names = {PurePosixPath(*name.parts[1:]) for name in names}
    manifest_name = PurePosixPath("MANIFEST.sha256")
    if manifest_name not in rel_names:
        raise SystemExit("Archive-local MANIFEST.sha256 is missing")

    forbidden_top = {"paper", "release-artifacts", ".git", ".lake", "site", "release"}
    forbidden_anywhere = {".git", ".lake", "__pycache__"}
    for rel in rel_names:
        if (rel.parts and rel.parts[0] in forbidden_top) or any(
            part in forbidden_anywhere for part in rel.parts
        ):
            raise SystemExit(f"Forbidden path in archive: {rel}")
        if rel.suffix.lower() in {".pdf", ".zip"}:
            raise SystemExit(f"Forbidden tracked binary in source archive: {rel}")

    required = {
        PurePosixPath("README.md"),
        PurePosixPath("MarkedRootedClosure/PaperTheorems.lean"),
        PurePosixPath("docs/paper/index.md"),
        PurePosixPath("docs/artifact/theorem-map.md"),
        PurePosixPath("archive/UPSTREAM.lock"),
        PurePosixPath("mkdocs.yml"),
    }
    missing = required - rel_names
    if missing:
        raise SystemExit("Missing required archive members: " + ", ".join(map(str, sorted(missing))))

    manifest_text = zf.read(f"{root}/MANIFEST.sha256").decode("utf-8")
    listed: dict[PurePosixPath, str] = {}
    for line in manifest_text.splitlines():
        if not line.strip():
            continue
        digest, rel_text = line.split("  ", 1)
        rel = PurePosixPath(rel_text)
        listed[rel] = digest
        member = f"{root}/{rel.as_posix()}"
        try:
            data = zf.read(member)
        except KeyError as exc:
            raise SystemExit(f"Manifest member missing from ZIP: {rel}") from exc
        got = hashlib.sha256(data).hexdigest()
        if got != digest:
            raise SystemExit(f"Manifest digest mismatch for {rel}")

    unlisted = rel_names - set(listed) - {manifest_name}
    if unlisted:
        raise SystemExit("Unlisted ZIP members: " + ", ".join(map(str, sorted(unlisted))))

print(f"release verification: OK ({zip_path.name})")
print(f"sha256: {actual}")
