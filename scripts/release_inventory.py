#!/usr/bin/env python3
"""Canonical release-asset inventory, checksums, and exact-set validation.

The release directory is a protocol boundary: generators, verifiers, CI artifact
transfer, and GitHub publication must agree on one ordered set of filenames.
Keeping that contract here prevents broad globs from silently publishing a
second copy of an asset or an unrelated file left in ``release/``.
"""
from __future__ import annotations

import hashlib
import os
import stat
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from project_config import release_stem


@dataclass(frozen=True)
class ArtifactSpec:
    """One primary release artifact recorded in the release index."""

    suffix: str
    role: str
    media_type: str


CORE_ARTIFACT_SPECS: tuple[ArtifactSpec, ...] = (
    ArtifactSpec(".zip", "source-archive", "application/zip"),
    ArtifactSpec(".spdx.json", "spdx-sbom", "application/spdx+json"),
    ArtifactSpec(
        ".cdx.json",
        "cyclonedx-sbom",
        "application/vnd.cyclonedx+json",
    ),
    ArtifactSpec(".buildinfo.json", "build-information", "application/json"),
    ArtifactSpec(
        ".intoto.jsonl",
        "in-toto-provenance",
        "application/jsonl",
    ),
)
INDEX_SPEC = ArtifactSpec(".release.json", "release-index", "application/json")
AGGREGATE_SUFFIX = ".checksums.sha256"


def sha256(path: Path) -> str:
    """Return the lowercase SHA-256 digest of *path*."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def artifact_path(release_dir: Path, stem: str, spec: ArtifactSpec) -> Path:
    return release_dir / f"{stem}{spec.suffix}"


def core_artifacts(
    project: dict[str, object], release_dir: Path
) -> tuple[tuple[Path, ArtifactSpec], ...]:
    """Return indexed release artifacts paired with their canonical metadata."""
    stem = release_stem(project)
    return tuple(
        (artifact_path(release_dir, stem, spec), spec)
        for spec in CORE_ARTIFACT_SPECS
    )


def core_artifact_paths(
    project: dict[str, object], release_dir: Path
) -> tuple[Path, ...]:
    return tuple(path for path, _ in core_artifacts(project, release_dir))


def index_path(project: dict[str, object], release_dir: Path) -> Path:
    return artifact_path(release_dir, release_stem(project), INDEX_SPEC)


def checksum_subject_paths(
    project: dict[str, object], release_dir: Path
) -> tuple[Path, ...]:
    """Artifacts covered by individual sidecars and the aggregate checksum."""
    return (*core_artifact_paths(project, release_dir), index_path(project, release_dir))


def sidecar_path(path: Path) -> Path:
    return path.with_suffix(path.suffix + ".sha256")


def aggregate_path(project: dict[str, object], release_dir: Path) -> Path:
    return release_dir / f"{release_stem(project)}{AGGREGATE_SUFFIX}"


def publication_paths(
    project: dict[str, object], release_dir: Path
) -> tuple[Path, ...]:
    """Return the complete, ordered set of files published on GitHub Releases."""
    subjects = checksum_subject_paths(project, release_dir)
    return (
        *subjects,
        *(sidecar_path(path) for path in subjects),
        aggregate_path(project, release_dir),
    )


def expected_release_names(project: dict[str, object]) -> tuple[str, ...]:
    return tuple(path.name for path in publication_paths(project, Path(".")))


def render_sidecar(path: Path) -> bytes:
    return f"{sha256(path)}  {path.name}\n".encode("utf-8")


def write_sidecar(path: Path) -> Path:
    out = sidecar_path(path)
    out.write_bytes(render_sidecar(path))
    return out


def verify_sidecar(path: Path) -> None:
    sidecar = sidecar_path(path)
    if not sidecar.is_file() or sidecar.is_symlink():
        raise ValueError(f"missing regular checksum sidecar: {sidecar}")
    expected = render_sidecar(path)
    actual = sidecar.read_bytes()
    if actual != expected:
        raise ValueError(f"non-canonical checksum sidecar: {sidecar.name}")


def render_aggregate(paths: Iterable[Path]) -> bytes:
    return b"".join(
        f"{sha256(path)}  {path.name}\n".encode("utf-8") for path in paths
    )


def _regular_file(path: Path) -> bool:
    try:
        mode = os.lstat(path).st_mode
    except OSError:
        return False
    return stat.S_ISREG(mode)


def verify_release_inventory(
    project: dict[str, object], release_dir: Path
) -> tuple[Path, ...]:
    """Require exactly the canonical release files and verify all checksums.

    Unexpected entries, missing files, directories, symlinks, non-regular files,
    malformed sidecars, and reordered or incomplete aggregate checksums fail.
    The strict byte comparison also enforces UTF-8, lowercase digests, two-space
    separators, canonical ordering, and a final LF.
    """
    if release_dir.is_symlink() or not release_dir.is_dir():
        raise ValueError(f"release directory is missing or not regular: {release_dir}")

    paths = publication_paths(project, release_dir)
    expected = {path.name for path in paths}
    entries = list(release_dir.iterdir())
    irregular = sorted(path.name for path in entries if not _regular_file(path))
    if irregular:
        raise ValueError(
            "release directory contains non-regular entries: " + ", ".join(irregular)
        )

    actual = {path.name for path in entries}
    missing = sorted(expected - actual)
    unexpected = sorted(actual - expected)
    if missing or unexpected:
        details: list[str] = []
        if missing:
            details.append("missing: " + ", ".join(missing))
        if unexpected:
            details.append("unexpected: " + ", ".join(unexpected))
        raise ValueError("release inventory mismatch (" + "; ".join(details) + ")")

    subjects = checksum_subject_paths(project, release_dir)
    for path in subjects:
        if not _regular_file(path):
            raise ValueError(f"release artifact is not a regular file: {path.name}")
        verify_sidecar(path)

    aggregate = aggregate_path(project, release_dir)
    expected_aggregate = render_aggregate(subjects)
    if aggregate.read_bytes() != expected_aggregate:
        raise ValueError(f"non-canonical aggregate checksum file: {aggregate.name}")
    return paths
