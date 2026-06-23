#!/usr/bin/env python3
"""Canonical source-tree inventory shared by manifests and release packaging."""
from __future__ import annotations

import hashlib
import os
import stat
import unicodedata
from difflib import unified_diff
from pathlib import Path
from typing import Sequence

MANIFEST_REL = Path("MANIFEST.sha256")
EXCLUDED_PREFIXES = frozenset(
    {
        ".git",
        ".lake",
        "site",
        "release",
        ".venv",
        ".venv-docs",
        ".oracle.log",
        "__pycache__",
        "docs/generated",
    }
)
EXCLUDED_DIR_NAMES = frozenset({"__pycache__", ".pytest_cache", ".mypy_cache"})
WINDOWS_FORBIDDEN_CHARS = frozenset('<>:"|?*')
WINDOWS_RESERVED_NAMES = frozenset(
    {"con", "prn", "aux", "nul", "clock$", "conin$", "conout$"}
    | {f"com{number}" for number in range(1, 10)}
    | {f"lpt{number}" for number in range(1, 10)}
)


class SourceInventoryError(ValueError):
    """Raised when the source tree cannot be packaged portably and safely."""


def is_excluded(rel: Path) -> bool:
    """Return whether *rel* is outside the distributable source tree."""
    value = rel.as_posix()
    return (
        any(value == item or value.startswith(item + "/") for item in EXCLUDED_PREFIXES)
        or any(part in EXCLUDED_DIR_NAMES for part in rel.parts)
    )


def _validate_relative_path(rel: Path) -> None:
    value = rel.as_posix()
    if rel.is_absolute() or not value or any(part in {"", ".", ".."} for part in rel.parts):
        raise SourceInventoryError(f"unsafe source path: {value!r}")
    if "\\" in value or any(unicodedata.category(char) == "Cc" for char in value):
        raise SourceInventoryError(f"non-portable source path: {value!r}")
    if unicodedata.normalize("NFC", value) != value:
        raise SourceInventoryError(f"source path is not Unicode NFC: {value!r}")
    for part in rel.parts:
        stem = part.split(".", 1)[0].casefold()
        if (
            part.endswith((" ", "."))
            or any(char in WINDOWS_FORBIDDEN_CHARS for char in part)
            or stem in WINDOWS_RESERVED_NAMES
        ):
            raise SourceInventoryError(f"non-portable source path: {value!r}")


def collect_source_files(root: Path, *, include_manifest: bool = True) -> list[Path]:
    """Return the validated, deterministic list of distributable source files.

    Included symlinks and non-regular filesystem entries are rejected before any
    file content is read. Case-insensitive/Unicode-normalized path collisions are
    rejected so the same archive cannot resolve to different trees on different
    filesystems.
    """
    root = root.resolve()
    files: list[Path] = []
    portable_prefixes: dict[tuple[str, ...], tuple[str, ...]] = {}

    def walk_error(error: OSError) -> None:
        raise SourceInventoryError(f"cannot scan source tree: {error}") from error

    for current, dirnames, filenames in os.walk(
        root, topdown=True, onerror=walk_error, followlinks=False
    ):
        current_path = Path(current)

        retained_dirs: list[str] = []
        for name in sorted(dirnames):
            path = current_path / name
            rel = path.relative_to(root)
            if is_excluded(rel):
                continue
            _validate_relative_path(rel)
            mode = os.lstat(path).st_mode
            if stat.S_ISLNK(mode):
                raise SourceInventoryError(
                    f"source-tree symlink is forbidden: {rel.as_posix()}"
                )
            if not stat.S_ISDIR(mode):
                raise SourceInventoryError(
                    f"non-directory source entry is forbidden: {rel.as_posix()}"
                )
            retained_dirs.append(name)
        dirnames[:] = retained_dirs

        for name in sorted(filenames):
            path = current_path / name
            rel = path.relative_to(root)
            if is_excluded(rel):
                continue
            _validate_relative_path(rel)

            mode = os.lstat(path).st_mode
            if stat.S_ISLNK(mode):
                raise SourceInventoryError(
                    f"source-tree symlink is forbidden: {rel.as_posix()}"
                )
            if not stat.S_ISREG(mode):
                raise SourceInventoryError(
                    f"non-regular source entry is forbidden: {rel.as_posix()}"
                )
            if not include_manifest and rel == MANIFEST_REL:
                continue

            for length in range(1, len(rel.parts) + 1):
                prefix = rel.parts[:length]
                portable_key = tuple(part.casefold() for part in prefix)
                previous = portable_prefixes.get(portable_key)
                if previous is not None and previous != prefix:
                    raise SourceInventoryError(
                        "portable source-path collision: "
                        f"{'/'.join(previous)!r} and {'/'.join(prefix)!r}"
                    )
                portable_prefixes[portable_key] = prefix
            files.append(path)

    return sorted(files, key=lambda path: path.relative_to(root).as_posix())


def render_manifest(root: Path, files: Sequence[Path] | None = None) -> bytes:
    """Render the canonical LF-terminated SHA-256 source manifest."""
    root = root.resolve()
    inventory = list(files) if files is not None else collect_source_files(
        root, include_manifest=False
    )
    rows: list[str] = []
    for path in inventory:
        rel = path.relative_to(root)
        if rel == MANIFEST_REL:
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        rows.append(f"{digest}  {rel.as_posix()}")
    return ("\n".join(rows) + "\n").encode("utf-8")


def write_manifest(root: Path) -> int:
    """Write the canonical source manifest and return its entry count."""
    root = root.resolve()
    files = collect_source_files(root, include_manifest=False)
    (root / MANIFEST_REL).write_bytes(render_manifest(root, files))
    return len(files)


def verify_manifest(root: Path) -> int:
    """Require the committed source manifest to match the current source tree."""
    root = root.resolve()
    manifest = root / MANIFEST_REL
    if not manifest.exists():
        raise SourceInventoryError("source manifest is missing; run `make manifest`")
    if manifest.is_symlink() or not manifest.is_file():
        raise SourceInventoryError("source manifest must be a regular file")

    files = collect_source_files(root, include_manifest=False)
    expected = render_manifest(root, files)
    actual = manifest.read_bytes()
    if actual != expected:
        try:
            actual_text = actual.decode("utf-8").splitlines()
        except UnicodeDecodeError as exc:
            raise SourceInventoryError("source manifest is not valid UTF-8") from exc
        expected_text = expected.decode("utf-8").splitlines()
        diff = list(
            unified_diff(
                actual_text,
                expected_text,
                fromfile="committed/MANIFEST.sha256",
                tofile="expected/MANIFEST.sha256",
                lineterm="",
            )
        )
        excerpt = "\n".join(diff[:80])
        suffix = "\n... diff truncated" if len(diff) > 80 else ""
        raise SourceInventoryError(
            "source manifest is stale; run `make manifest` and review the diff"
            + (f"\n{excerpt}{suffix}" if excerpt else "")
        )
    return len(files)
