#!/usr/bin/env python3
"""Shared, validated project metadata helpers for repository tooling."""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROJECT_FILE = ROOT / "project.json"
SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def load_project(root: Path = ROOT) -> dict[str, Any]:
    """Load project.json and enforce the publication-artifact invariants."""
    path = root / "project.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    required = {
        "schema_version",
        "version",
        "release_date",
        "artifact_title",
        "site_name",
        "site_tagline",
        "repository_owner",
        "repository_slug",
        "recommended_repository_slug",
        "lean_package",
        "upstream_repository",
        "upstream_commit",
        "lean_toolchain",
        "mathlib_commit",
        "publication_model",
        "paper_entrypoint",
        "rename_status",
        "minimum_python",
        "release_profile",
        "elan_installer_commit",
        "elan_installer_blob_sha",
        "python_lock",
        "citation_schema",
        "proof_dag",
        "provenance_format",
    }
    missing = sorted(required - data.keys())
    if missing:
        raise ValueError(f"project.json is missing fields: {', '.join(missing)}")
    if data["schema_version"] != 4:
        raise ValueError("project.json schema_version must be 4")
    if not SEMVER_RE.fullmatch(data["version"]):
        raise ValueError(f"invalid semantic version: {data['version']!r}")
    try:
        date.fromisoformat(data["release_date"])
    except ValueError as exc:
        raise ValueError(f"invalid release_date: {data['release_date']!r}") from exc
    for key in ("repository_slug", "recommended_repository_slug"):
        if not SLUG_RE.fullmatch(data[key]):
            raise ValueError(f"invalid repository slug: {key}={data[key]!r}")
    if data["rename_status"] != "adopted":
        raise ValueError("the public repository rename must be recorded as adopted")
    if data["repository_slug"] != data["recommended_repository_slug"]:
        raise ValueError("adopted and recommended repository slugs must agree")
    for key in ("upstream_commit", "mathlib_commit", "elan_installer_commit", "elan_installer_blob_sha"):
        if not SHA_RE.fullmatch(data[key]):
            raise ValueError(f"invalid commit pin: {key}={data[key]!r}")
    if data["minimum_python"] != "3.11":
        raise ValueError("minimum_python must remain 3.11 for this release line")
    if data["release_profile"] != "source-only-reproducible":
        raise ValueError("release_profile must remain source-only-reproducible")
    if data["publication_model"] != "integrated-documentation":
        raise ValueError("publication_model must remain integrated-documentation")
    if data["paper_entrypoint"] != "docs/paper/index.md":
        raise ValueError("paper_entrypoint must remain docs/paper/index.md")
    expected_paths = {
        "python_lock": "requirements-docs.lock",
        "citation_schema": "schemas/citation-cff.schema.json",
        "proof_dag": "archive/proof-dag.json",
    }
    for key, expected in expected_paths.items():
        if data[key] != expected:
            raise ValueError(f"{key} must remain {expected}")
        if not (root / expected).is_file():
            raise ValueError(f"project metadata path is missing: {expected}")
    if data["provenance_format"] != "in-toto-statement-v1":
        raise ValueError("provenance_format must remain in-toto-statement-v1")
    return data


def repository_full_name(project: dict[str, Any]) -> str:
    return f"{project['repository_owner']}/{project['repository_slug']}"


def repository_url(project: dict[str, Any]) -> str:
    return f"https://github.com/{repository_full_name(project)}"


def site_url(project: dict[str, Any]) -> str:
    return f"https://{project['repository_owner']}.github.io/{project['repository_slug']}/"


def release_stem(project: dict[str, Any]) -> str:
    return f"{project['repository_slug']}-v{project['version']}"
