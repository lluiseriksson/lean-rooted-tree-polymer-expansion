#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
import zipfile
from pathlib import Path, PurePosixPath

from project_config import ROOT, load_project, release_stem

project = load_project()
release_dir = ROOT / "release"
stem = release_stem(project)

if len(sys.argv) > 1:
    zip_path = Path(sys.argv[1]).resolve()
else:
    zip_path = release_dir / f"{stem}.zip"
if not zip_path.is_file():
    raise SystemExit(f"No release ZIP found: {zip_path}")

sidecar = zip_path.with_suffix(zip_path.suffix + ".sha256")
if not sidecar.is_file():
    raise SystemExit(f"Missing SHA-256 sidecar: {sidecar}")
expected = sidecar.read_text(encoding="utf-8").split()[0]
actual = hashlib.sha256(zip_path.read_bytes()).hexdigest()
if expected != actual:
    raise SystemExit(f"ZIP digest mismatch: expected {expected}, got {actual}")

with zipfile.ZipFile(zip_path) as archive:
    bad = archive.testzip()
    if bad:
        raise SystemExit(f"Corrupt ZIP member: {bad}")
    infos = [info for info in archive.infolist() if not info.is_dir()]
    names = [PurePosixPath(info.filename) for info in infos]
    roots = {name.parts[0] for name in names if name.parts}
    if roots != {stem}:
        raise SystemExit(f"Archive root mismatch: expected {stem}, found {roots}")
    rel_names = {PurePosixPath(*name.parts[1:]) for name in names}
    manifest_name = PurePosixPath("MANIFEST.sha256")
    if manifest_name not in rel_names:
        raise SystemExit("Archive-local MANIFEST.sha256 is missing")

    forbidden_top = {
        "paper", "release-artifacts", ".git", ".lake", "site", "release",
        "docs/generated",
    }
    forbidden_anywhere = {".git", ".lake", "__pycache__"}
    for rel in rel_names:
        text = rel.as_posix()
        if any(text == item or text.startswith(item + "/") for item in forbidden_top):
            raise SystemExit(f"Forbidden path in archive: {rel}")
        if any(part in forbidden_anywhere for part in rel.parts):
            raise SystemExit(f"Forbidden path in archive: {rel}")
        if rel.suffix.lower() in {".pdf", ".zip"}:
            raise SystemExit(f"Forbidden tracked binary in source archive: {rel}")

    required = {
        PurePosixPath("README.md"),
        PurePosixPath("project.json"),
        PurePosixPath("REPOSITORY_RENAME.md"),
        PurePosixPath("lake-manifest.json"),
        PurePosixPath("MarkedRootedClosure/PaperTheorems.lean"),
        PurePosixPath("docs/paper/index.md"),
        PurePosixPath("docs/paper/manifest.json"),
        PurePosixPath("docs/formalization/index.md"),
        PurePosixPath("docs/artifact/theorem-map.md"),
        PurePosixPath("archive/UPSTREAM.lock"),
        PurePosixPath("archive/theorem-manifest.json"),
        PurePosixPath("mkdocs.yml"),
    }
    missing = required - rel_names
    if missing:
        raise SystemExit("Missing required archive members: " + ", ".join(map(str, sorted(missing))))

    manifest_text = archive.read(f"{stem}/MANIFEST.sha256").decode("utf-8")
    listed: dict[PurePosixPath, str] = {}
    for line in manifest_text.splitlines():
        if not line.strip():
            continue
        digest, rel_text = line.split("  ", 1)
        rel = PurePosixPath(rel_text)
        listed[rel] = digest
        member = f"{stem}/{rel.as_posix()}"
        try:
            data = archive.read(member)
        except KeyError as exc:
            raise SystemExit(f"Manifest member missing from ZIP: {rel}") from exc
        got = hashlib.sha256(data).hexdigest()
        if got != digest:
            raise SystemExit(f"Manifest digest mismatch for {rel}")

    unlisted = rel_names - set(listed) - {manifest_name}
    if unlisted:
        raise SystemExit("Unlisted ZIP members: " + ", ".join(map(str, sorted(unlisted))))

    archived_project = json.loads(archive.read(f"{stem}/project.json"))
    if archived_project["version"] != project["version"]:
        raise SystemExit("archived project version mismatch")
    archived_lake = json.loads(archive.read(f"{stem}/lake-manifest.json"))
    revisions = {pkg["name"]: pkg["rev"] for pkg in archived_lake["packages"]}
    if revisions.get("YangMills") != project["upstream_commit"]:
        raise SystemExit("archived upstream dependency mismatch")
    if revisions.get("mathlib") != project["mathlib_commit"]:
        raise SystemExit("archived Mathlib dependency mismatch")

print(f"release verification: OK ({zip_path.name})")
print(f"sha256: {actual}")
