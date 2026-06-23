#!/usr/bin/env python3
"""Check release version and date consistency across machine and prose metadata."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from project_config import ROOT, load_project


def _yaml(path: Path) -> dict[str, Any]:
    import yaml  # type: ignore
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected YAML object: {path}")
    return value


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    project = load_project(root)
    version = project["version"]
    date = project["release_date"]

    json_expectations = {
        "codemeta.json": ("version", version),
        ".zenodo.json": ("version", version),
        "archive/theorem-manifest.json": ("version", version),
        "archive/proof-dag.json": ("version", version),
    }
    for rel, (key, expected) in json_expectations.items():
        try:
            value = json.loads((root / rel).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"cannot read {rel}: {exc}")
            continue
        if value.get(key) != expected:
            errors.append(f"{rel}:{key} differs from project.json")
    for rel, key in (("codemeta.json", "datePublished"), (".zenodo.json", "publication_date")):
        value = json.loads((root / rel).read_text(encoding="utf-8"))
        if value.get(key) != date:
            errors.append(f"{rel}:{key} differs from project.json")

    try:
        citation = _yaml(root / "CITATION.cff")
        submission = _yaml(root / "docs/publication/submission-metadata.yaml")
    except (OSError, ValueError) as exc:
        errors.append(str(exc))
    else:
        if str(citation.get("version")) != version:
            errors.append("CITATION.cff version differs from project.json")
        if str(citation.get("date-released")) != date:
            errors.append("CITATION.cff date differs from project.json")
        if str(submission.get("version")) != version:
            errors.append("submission metadata version differs from project.json")
        if str(submission.get("date")) != date:
            errors.append("submission metadata date differs from project.json")

    lake = (root / "lakefile.lean").read_text(encoding="utf-8")
    if f'version := v!"{version}"' not in lake:
        errors.append("lakefile.lean package version differs from project.json")
    bib = (root / "CITATION.bib").read_text(encoding="utf-8")
    if not re.search(rf"version\s*=\s*\{{{re.escape(version)}\}}", bib):
        errors.append("CITATION.bib version differs from project.json")

    text_expectations = {
        "README.md": f"`v{version}`",
        "RELEASE_NOTES.md": f"# Release notes: v{version}",
        "MIGRATION.md": f"# Migration to v{version}",
        "docs/llms.txt": f"Version: {version}",
        "docs/maintainers/repository-audit.md": f"v{version}",
    }
    for rel, needle in text_expectations.items():
        try:
            text = (root / rel).read_text(encoding="utf-8")
        except OSError as exc:
            errors.append(f"cannot read {rel}: {exc}")
            continue
        if needle not in text:
            errors.append(f"{rel} missing current release marker {needle!r}")

    changelog = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    if f"## {version} - {date}" not in changelog:
        errors.append("CHANGELOG.md lacks current version/date heading")
    return errors


def main() -> None:
    errors = validate()
    if errors:
        raise SystemExit("Version consistency audit failed:\n" + "\n".join(f"- {e}" for e in errors))
    project = load_project()
    print(f"version consistency audit: OK (v{project['version']} · {project['release_date']})")


if __name__ == "__main__":
    main()
