#!/usr/bin/env python3
"""Validate the direct and fully resolved documentation dependency locks."""
from __future__ import annotations

from project_config import ROOT
from python_requirements import requirement_map

DIRECT = ROOT / "requirements-docs.txt"
LOCK = ROOT / "requirements-docs.lock"
FORBIDDEN = {"cffconvert", "mkdocs-minify-plugin", "csscompressor", "jsmin", "htmlmin2"}
REQUIRED_DIRECT = {"mkdocs", "mkdocs-material", "jsonschema", "pyyaml"}


def validate(root=ROOT) -> list[str]:
    errors: list[str] = []
    try:
        direct = requirement_map(root / DIRECT.name)
        locked = requirement_map(root / LOCK.name)
    except (OSError, ValueError) as exc:
        return [str(exc)]

    if set(direct) != REQUIRED_DIRECT:
        errors.append(
            "direct documentation dependency set mismatch: "
            + ", ".join(sorted(set(direct) ^ REQUIRED_DIRECT))
        )
    for canonical, (name, version) in direct.items():
        locked_record = locked.get(canonical)
        if locked_record is None:
            errors.append(f"direct requirement missing from lock: {name}=={version}")
        elif locked_record[1] != version:
            errors.append(
                f"direct/lock version mismatch for {name}: {version} != {locked_record[1]}"
            )
    present_forbidden = FORBIDDEN & set(locked)
    if present_forbidden:
        errors.append("forbidden or superseded packages in lock: " + ", ".join(sorted(present_forbidden)))
    if len(locked) < len(direct):
        errors.append("transitive lock is unexpectedly smaller than direct requirements")
    return errors


def main() -> None:
    errors = validate()
    if errors:
        raise SystemExit("Python dependency lock audit failed:\n" + "\n".join(f"- {e}" for e in errors))
    direct = requirement_map(DIRECT)
    locked = requirement_map(LOCK)
    print(f"Python dependency lock audit: OK ({len(direct)} direct; {len(locked)} total)")


if __name__ == "__main__":
    main()
