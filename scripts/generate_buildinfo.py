#!/usr/bin/env python3
"""Generate deterministic build information for the archive and both SBOMs."""
from __future__ import annotations

import json
from pathlib import Path

from project_config import ROOT, load_project, release_stem, repository_url, site_url
from release_inventory import sha256, write_sidecar



def digest_record(path: Path, media_type: str) -> dict[str, object]:
    return {
        "name": path.name,
        "media_type": media_type,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def source_record(path: Path) -> dict[str, str]:
    return {"path": path.relative_to(ROOT).as_posix(), "sha256": sha256(path)}


def main() -> None:
    project = load_project()
    release_dir = ROOT / "release"
    stem = release_stem(project)
    zip_path = release_dir / f"{stem}.zip"
    spdx_path = release_dir / f"{stem}.spdx.json"
    cdx_path = release_dir / f"{stem}.cdx.json"
    required = [zip_path, spdx_path, cdx_path]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit("build-info inputs missing: " + ", ".join(missing))

    source_inputs = {
        "python_lock": ROOT / project["python_lock"],
        "theorem_manifest": ROOT / "archive/theorem-manifest.json",
        "proof_dag": ROOT / project["proof_dag"],
        "paper_manifest": ROOT / "docs/paper/manifest.json",
        "actions_manifest": ROOT / "archive/actions-manifest.json",
        "source_manifest": ROOT / "MANIFEST.sha256",
        "citation_schema": ROOT / project["citation_schema"],
    }
    data = {
        "schema_version": 2,
        "project": {
            "name": project["repository_slug"],
            "version": project["version"],
            "release_date": project["release_date"],
            "repository": repository_url(project),
            "documentation": site_url(project),
            "publication_model": project["publication_model"],
            "release_profile": project["release_profile"],
            "minimum_python": project["minimum_python"],
            "python_lock": project["python_lock"],
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
        "source_inputs": {
            name: source_record(path) for name, path in source_inputs.items()
        },
        "artifacts": [
            digest_record(zip_path, "application/zip"),
            digest_record(spdx_path, "application/spdx+json"),
            digest_record(cdx_path, "application/vnd.cyclonedx+json"),
        ],
        "verification": {
            "source_commands": [
                "make verify-nonlean",
                "leanprover/lean-action build MarkedRootedClosure",
                "make lean-oracle",
                "make package-determinism",
                "make smoke-release",
            ],
            "axiom_policy": ["propext", "Classical.choice", "Quot.sound"],
            "standalone_pdf_tracked": False,
            "ci_python": "3.12",
        },
    }
    out = release_dir / f"{stem}.buildinfo.json"
    out.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    digest = sha256(out)
    write_sidecar(out)
    print(f"build info created: {out}")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
