#!/usr/bin/env python3
"""Generate a deterministic in-toto Statement v1 with SLSA provenance v1."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from project_config import ROOT, load_project, release_stem, repository_url, site_url
from release_inventory import sha256, write_sidecar



def subject(path: Path) -> dict[str, object]:
    return {"name": path.name, "digest": {"sha256": sha256(path)}}


def dependency(uri: str, algorithm: str, digest: str) -> dict[str, object]:
    return {"uri": uri, "digest": {algorithm: digest}}


def build_statement(
    project: dict[str, Any],
    subjects: list[Path],
    source_inputs: dict[str, Path],
) -> dict[str, object]:
    """Build the deterministic declaration; hosted CI attests execution separately."""
    return {
        "_type": "https://in-toto.io/Statement/v1",
        "subject": [subject(path) for path in subjects],
        "predicateType": "https://slsa.dev/provenance/v1",
        "predicate": {
            "buildDefinition": {
                "buildType": site_url(project) + "build-types/source-release-v1",
                "externalParameters": {
                    "repository": repository_url(project),
                    "version": project["version"],
                    "releaseDate": project["release_date"],
                    "publicationModel": project["publication_model"],
                    "releaseProfile": project["release_profile"],
                },
                "internalParameters": {
                    "releaseRecipe": ["make package-determinism"],
                    "requiredExternalGates": [
                        "leanprover/lean-action build MarkedRootedClosure",
                        "make lean-oracle",
                    ],
                    "sourceInputs": {
                        name: {
                            "path": path.relative_to(ROOT).as_posix(),
                            "sha256": sha256(path),
                        }
                        for name, path in source_inputs.items()
                    },
                },
                "resolvedDependencies": [
                    dependency(
                        project["upstream_repository"] + ".git",
                        "gitCommit",
                        project["upstream_commit"],
                    ),
                    dependency(
                        "https://github.com/leanprover-community/mathlib4.git",
                        "gitCommit",
                        project["mathlib_commit"],
                    ),
                    dependency(
                        "https://github.com/leanprover/elan/blob/"
                        + project["elan_installer_commit"]
                        + "/elan-init.sh",
                        "gitBlob",
                        project["elan_installer_blob_sha"],
                    ),
                    dependency(
                        "file:" + project["python_lock"],
                        "sha256",
                        sha256(ROOT / project["python_lock"]),
                    ),
                    dependency(
                        "file:archive/actions-manifest.json",
                        "sha256",
                        sha256(ROOT / "archive/actions-manifest.json"),
                    ),
                ],
            },
            "runDetails": {
                "builder": {
                    "id": site_url(project)
                    + "builders/deterministic-source-tooling-v1"
                },
                "metadata": {
                    "invocationId": "deterministic-source-release-v"
                    + project["version"],
                    "reproducible": True,
                    "executionBound": False,
                    "hostedAttestationRequired": True,
                },
            },
        },
    }


def main() -> None:
    project = load_project()
    release_dir = ROOT / "release"
    stem = release_stem(project)
    subjects = [
        release_dir / f"{stem}.zip",
        release_dir / f"{stem}.spdx.json",
        release_dir / f"{stem}.cdx.json",
        release_dir / f"{stem}.buildinfo.json",
    ]
    missing = [str(path) for path in subjects if not path.is_file()]
    if missing:
        raise SystemExit("provenance inputs missing: " + ", ".join(missing))

    source_inputs = {
        "python_lock": ROOT / project["python_lock"],
        "theorem_manifest": ROOT / "archive/theorem-manifest.json",
        "proof_dag": ROOT / project["proof_dag"],
        "paper_manifest": ROOT / "docs/paper/manifest.json",
        "actions_manifest": ROOT / "archive/actions-manifest.json",
        "citation_schema": ROOT / project["citation_schema"],
        "source_manifest": ROOT / "MANIFEST.sha256",
    }
    statement = build_statement(project, subjects, source_inputs)
    out = release_dir / f"{stem}.intoto.jsonl"
    out.write_text(
        json.dumps(statement, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    digest = sha256(out)
    write_sidecar(out)
    print(f"in-toto provenance created: {out}")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
