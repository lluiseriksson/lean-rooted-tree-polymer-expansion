#!/usr/bin/env python3
"""Shared project metadata helpers for repository tooling."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROJECT_FILE = ROOT / "project.json"


def load_project(root: Path = ROOT) -> dict[str, Any]:
    data = json.loads((root / "project.json").read_text(encoding="utf-8"))
    required = {
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
    }
    missing = sorted(required - data.keys())
    if missing:
        raise ValueError(f"project.json is missing fields: {', '.join(missing)}")
    return data


def repository_full_name(project: dict[str, Any]) -> str:
    return f"{project['repository_owner']}/{project['repository_slug']}"


def repository_url(project: dict[str, Any]) -> str:
    return f"https://github.com/{repository_full_name(project)}"


def site_url(project: dict[str, Any]) -> str:
    return (
        f"https://{project['repository_owner']}.github.io/"
        f"{project['repository_slug']}/"
    )


def release_stem(project: dict[str, Any]) -> str:
    return f"{project['repository_slug']}-v{project['version']}"
