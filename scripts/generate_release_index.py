#!/usr/bin/env python3
"""Generate one machine-readable index and aggregate checksum list for a release."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from project_config import ROOT, load_project, release_stem, repository_url, site_url


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record(path: Path, role: str, media_type: str) -> dict[str, object]:
    return {
        "name": path.name,
        "role": role,
        "media_type": media_type,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def evidence(path: Path) -> dict[str, str]:
    return {"path": path.relative_to(ROOT).as_posix(), "sha256": sha256(path)}


def main() -> None:
    project = load_project()
    release_dir = ROOT / "release"
    stem = release_stem(project)
    files = [
        (release_dir / f"{stem}.zip", "source-archive", "application/zip"),
        (release_dir / f"{stem}.spdx.json", "spdx-sbom", "application/spdx+json"),
        (release_dir / f"{stem}.cdx.json", "cyclonedx-sbom", "application/vnd.cyclonedx+json"),
        (release_dir / f"{stem}.buildinfo.json", "build-information", "application/json"),
        (release_dir / f"{stem}.intoto.jsonl", "in-toto-provenance", "application/jsonl"),
    ]
    missing = [str(path) for path, _, _ in files if not path.is_file()]
    if missing:
        raise SystemExit("release-index inputs missing: " + ", ".join(missing))

    source_files = {
        "project_metadata": ROOT / "project.json",
        "theorem_manifest": ROOT / "archive/theorem-manifest.json",
        "proof_dag": ROOT / project["proof_dag"],
        "paper_manifest": ROOT / "docs/paper/manifest.json",
        "actions_manifest": ROOT / "archive/actions-manifest.json",
        "python_lock": ROOT / project["python_lock"],
        "citation_schema": ROOT / project["citation_schema"],
        "source_manifest": ROOT / "MANIFEST.sha256",
    }
    data = {
        "schema_version": 2,
        "release": {
            "name": stem,
            "version": project["version"],
            "date": project["release_date"],
            "repository": repository_url(project),
            "documentation": site_url(project),
            "profile": project["release_profile"],
            "provenance_format": project["provenance_format"],
        },
        "proof_environment": {
            "lean_toolchain": project["lean_toolchain"],
            "mathlib_commit": project["mathlib_commit"],
            "upstream_repository": project["upstream_repository"],
            "upstream_commit": project["upstream_commit"],
            "elan_installer_commit": project["elan_installer_commit"],
            "elan_installer_blob_sha": project["elan_installer_blob_sha"],
        },
        "source_evidence": {
            name: evidence(path) for name, path in source_files.items()
        },
        "artifacts": [record(path, role, media) for path, role, media in files],
    }
    index_path = release_dir / f"{stem}.release.json"
    index_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    index_digest = sha256(index_path)
    index_path.with_suffix(index_path.suffix + ".sha256").write_text(
        f"{index_digest}  {index_path.name}\n", encoding="utf-8"
    )

    checksum_paths = [path for path, _, _ in files] + [index_path]
    checksums_path = release_dir / f"{stem}.checksums.sha256"
    checksums_path.write_text(
        "".join(f"{sha256(path)}  {path.name}\n" for path in checksum_paths),
        encoding="utf-8",
    )
    print(f"release index created: {index_path}")
    print(f"aggregate checksums created: {checksums_path}")


if __name__ == "__main__":
    main()
