#!/usr/bin/env python3
"""Safely update release identity files; changelog prose remains maintainer-authored."""
from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path

from project_config import ROOT, load_project

SEMVER = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")


def _write_json(path: Path, data: object, dry_run: bool) -> None:
    if not dry_run:
        path.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def _replace(path: Path, old: str, new: str, dry_run: bool, *, count: int = 0) -> None:
    text = path.read_text(encoding="utf-8")
    occurrences = text.count(old)
    if occurrences == 0:
        raise ValueError(f"expected marker not found in {path}: {old!r}")
    updated = text.replace(old, new, count) if count else text.replace(old, new)
    if not dry_run:
        path.write_text(updated, encoding="utf-8")


def bump(root: Path, new_version: str, new_date: str, dry_run: bool = False) -> None:
    if not SEMVER.fullmatch(new_version):
        raise ValueError(f"invalid semantic version: {new_version}")
    date.fromisoformat(new_date)
    project = load_project(root)
    old_version = project["version"]
    old_date = project["release_date"]
    if new_version == old_version:
        raise ValueError("new version equals current version")

    project["version"] = new_version
    project["release_date"] = new_date
    _write_json(root / "project.json", project, dry_run)

    for rel, version_key, date_key in (
        ("codemeta.json", "version", "datePublished"),
        (".zenodo.json", "version", "publication_date"),
    ):
        path = root / rel
        data = json.loads(path.read_text(encoding="utf-8"))
        data[version_key] = new_version
        data[date_key] = new_date
        _write_json(path, data, dry_run)
    for rel in ("archive/theorem-manifest.json", "archive/proof-dag.json"):
        path = root / rel
        data = json.loads(path.read_text(encoding="utf-8"))
        data["version"] = new_version
        _write_json(path, data, dry_run)

    _replace(root / "lakefile.lean", f'version := v!"{old_version}"', f'version := v!"{new_version}"', dry_run, count=1)
    _replace(root / "CITATION.cff", f"version: {old_version}", f"version: {new_version}", dry_run, count=1)
    _replace(root / "CITATION.cff", f"date-released: {old_date}", f"date-released: {new_date}", dry_run, count=1)
    _replace(root / "CITATION.bib", f"version      = {{{old_version}}}", f"version      = {{{new_version}}}", dry_run, count=1)
    _replace(root / "docs/publication/submission-metadata.yaml", f'version: "{old_version}"', f'version: "{new_version}"', dry_run, count=1)
    _replace(root / "docs/publication/submission-metadata.yaml", f'date: "{old_date}"', f'date: "{new_date}"', dry_run, count=1)
    _replace(root / "docs/llms.txt", f"Version: {old_version}", f"Version: {new_version}", dry_run, count=1)

    for rel in (
        "README.md",
        "RELEASE_NOTES.md",
        "MIGRATION.md",
        "ROADMAP.md",
        "docs/about/citation.md",
        "docs/artifact/build-status.md",
        "docs/maintainers/agent-handoff.md",
        "docs/maintainers/release-playbook.md",
        "docs/maintainers/repository-audit.md",
        "docs/maintainers/upload-and-migration.md",
        "docs/publication/submission-checklist.md",
    ):
        _replace(root / rel, old_version, new_version, dry_run)
    print(
        f"{'would update' if dry_run else 'updated'} release identity: "
        f"v{old_version} ({old_date}) -> v{new_version} ({new_date})"
    )
    print("maintainer action required: add the new CHANGELOG.md entry before verification")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("version")
    parser.add_argument("--date", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    bump(ROOT, args.version, args.date, args.dry_run)


if __name__ == "__main__":
    main()
