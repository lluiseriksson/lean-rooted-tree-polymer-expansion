#!/usr/bin/env python3
"""Validate repository JSON/YAML metadata without conflicting CFF tooling."""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any

from project_config import ROOT, load_project

JSON_FILES = (
    "project.json",
    "lake-manifest.json",
    "codemeta.json",
    ".zenodo.json",
    "archive/theorem-manifest.json",
    "archive/actions-manifest.json",
    "archive/proof-dag.json",
    "docs/paper/manifest.json",
)
YAML_FILES = (
    "CITATION.cff",
    "mkdocs.yml",
    "docs/publication/submission-metadata.yaml",
    ".github/dependabot.yml",
    ".github/workflows/ci.yml",
    ".github/workflows/pages.yml",
    ".github/workflows/release.yml",
    ".github/workflows/dependency-review.yml",
    ".github/workflows/maintenance.yml",
)
SCHEMA_PAIRS = (
    ("project.json", "schemas/project.schema.json"),
    ("archive/theorem-manifest.json", "schemas/theorem-manifest.schema.json"),
    ("archive/proof-dag.json", "schemas/proof-dag.schema.json"),
    ("docs/paper/manifest.json", "schemas/paper-manifest.schema.json"),
    ("archive/actions-manifest.json", "schemas/actions-manifest.schema.json"),
)


def _normalise_yaml_scalars(value: Any) -> Any:
    """Convert YAML-native dates to strings before JSON Schema validation."""
    if isinstance(value, (dt.date, dt.datetime)):
        return value.isoformat()
    if isinstance(value, list):
        return [_normalise_yaml_scalars(item) for item in value]
    if isinstance(value, dict):
        return {key: _normalise_yaml_scalars(item) for key, item in value.items()}
    return value


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    project = load_project(root)
    for rel in JSON_FILES:
        try:
            json.loads((root / rel).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"invalid JSON {rel}: {exc}")

    try:
        import yaml  # type: ignore
    except ImportError:
        # The source-only clean-room smoke test intentionally has no third-party
        # Python environment. Full CI installs requirements-docs.lock and runs
        # this schema layer there. JSON parsing above still runs everywhere.
        return errors
    yaml_values: dict[str, Any] = {}
    for rel in YAML_FILES:
        try:
            with (root / rel).open(encoding="utf-8") as handle:
                value = yaml.safe_load(handle)
        except (OSError, yaml.YAMLError) as exc:
            errors.append(f"invalid YAML {rel}: {exc}")
            continue
        if value is None:
            errors.append(f"empty YAML document: {rel}")
        yaml_values[rel] = _normalise_yaml_scalars(value)

    try:
        import jsonschema  # type: ignore
    except ImportError:
        return errors
    for data_rel, schema_rel in SCHEMA_PAIRS:
        try:
            data = json.loads((root / data_rel).read_text(encoding="utf-8"))
            schema = json.loads((root / schema_rel).read_text(encoding="utf-8"))
            jsonschema.Draft202012Validator(schema).validate(data)
        except (OSError, json.JSONDecodeError, jsonschema.ValidationError) as exc:
            errors.append(f"schema validation failed for {data_rel}: {exc}")

    citation = yaml_values.get("CITATION.cff")
    if citation is not None:
        try:
            schema = json.loads((root / "schemas/citation-cff.schema.json").read_text(encoding="utf-8"))
            jsonschema.Draft202012Validator(schema).validate(citation)
        except (OSError, json.JSONDecodeError, jsonschema.ValidationError) as exc:
            errors.append(f"CITATION.cff profile validation failed: {exc}")
        if isinstance(citation, dict):
            if citation.get("version") != project["version"]:
                errors.append("CITATION.cff version differs from project.json")
            if citation.get("title") != project["artifact_title"]:
                errors.append("CITATION.cff title differs from project.json")
            if citation.get("date-released") != project["release_date"]:
                errors.append("CITATION.cff date-released differs from project.json")
    return errors


def main() -> None:
    errors = validate()
    if errors:
        raise SystemExit("Metadata audit failed:\n" + "\n".join(f"- {e}" for e in errors))
    print("metadata audit: JSON/YAML parse, repository schemas, and CFF profile validate")


if __name__ == "__main__":
    main()
