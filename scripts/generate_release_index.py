#!/usr/bin/env python3
"""Generate the release index and canonical checksum inventory."""
from __future__ import annotations

import json
from pathlib import Path

from project_config import ROOT, load_project, release_stem, repository_url, site_url
from release_inventory import (
    aggregate_path,
    checksum_subject_paths,
    core_artifacts,
    index_path,
    render_aggregate,
    sha256,
    verify_release_inventory,
    write_sidecar,
)


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
    files = core_artifacts(project, release_dir)
    missing = [str(path) for path, _ in files if not path.is_file()]
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
        "artifacts": [
            record(path, spec.role, spec.media_type) for path, spec in files
        ],
    }
    release_index = index_path(project, release_dir)
    release_index.write_text(
        json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    write_sidecar(release_index)

    checksums = aggregate_path(project, release_dir)
    checksums.write_bytes(render_aggregate(checksum_subject_paths(project, release_dir)))
    verify_release_inventory(project, release_dir)
    print(f"release index created: {release_index}")
    print(f"aggregate checksums created: {checksums}")


if __name__ == "__main__":
    main()
