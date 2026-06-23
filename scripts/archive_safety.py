#!/usr/bin/env python3
"""Bounded, path-safe extraction helpers for verified source ZIP archives."""
from __future__ import annotations

import os
import stat
import unicodedata
import zipfile
from pathlib import Path, PurePosixPath

MAX_MEMBER_BYTES = 10 * 1024 * 1024
MAX_TOTAL_BYTES = 50 * 1024 * 1024
WINDOWS_FORBIDDEN_CHARS = frozenset('<>:"|?*')
WINDOWS_RESERVED_NAMES = frozenset(
    {"con", "prn", "aux", "nul", "clock$", "conin$", "conout$"}
    | {f"com{number}" for number in range(1, 10)}
    | {f"lpt{number}" for number in range(1, 10)}
)


def _validated_portable_path(raw_name: str) -> PurePosixPath:
    if unicodedata.normalize("NFC", raw_name) != raw_name:
        raise ValueError(f"non-NFC archive path: {raw_name!r}")
    name = PurePosixPath(raw_name)
    if (
        not raw_name
        or name.is_absolute()
        or raw_name != name.as_posix()
        or any(part in {"", ".", ".."} for part in name.parts)
        or "\\" in raw_name
        or any(unicodedata.category(char) == "Cc" for char in raw_name)
    ):
        raise ValueError(f"unsafe archive path: {raw_name!r}")
    for part in name.parts:
        stem = part.split(".", 1)[0].casefold()
        if (
            part.endswith((" ", "."))
            or any(char in WINDOWS_FORBIDDEN_CHARS for char in part)
            or stem in WINDOWS_RESERVED_NAMES
        ):
            raise ValueError(f"non-portable archive path: {raw_name!r}")
    return name


def validated_members(archive: zipfile.ZipFile) -> list[zipfile.ZipInfo]:
    infos = [info for info in archive.infolist() if not info.is_dir()]
    raw_names = [info.filename for info in infos]
    if len(raw_names) != len(set(raw_names)):
        raise ValueError("duplicate ZIP member name")

    names = [_validated_portable_path(raw_name) for raw_name in raw_names]
    folded = [tuple(part.casefold() for part in name.parts) for name in names]
    if len(folded) != len(set(folded)):
        raise ValueError("case-insensitive collision in ZIP member names")

    portable_prefixes: dict[tuple[str, ...], tuple[str, ...]] = {}
    file_paths = {name.parts for name in names}
    for name in names:
        parts = name.parts
        for length in range(1, len(parts) + 1):
            prefix = parts[:length]
            key = tuple(part.casefold() for part in prefix)
            previous = portable_prefixes.get(key)
            if previous is not None and previous != prefix:
                raise ValueError(
                    "case-insensitive path-component collision in ZIP: "
                    f"{'/'.join(previous)!r} and {'/'.join(prefix)!r}"
                )
            portable_prefixes[key] = prefix
        if any(parts[:length] in file_paths for length in range(1, len(parts))):
            raise ValueError(f"file/directory collision in ZIP path: {name}")

    total = 0
    for info, name in zip(infos, names):
        mode = (info.external_attr >> 16) & 0xFFFF
        kind = stat.S_IFMT(mode)
        if kind == stat.S_IFLNK:
            raise ValueError(f"symlink forbidden in source archive: {name}")
        if kind not in (0, stat.S_IFREG):
            raise ValueError(f"non-regular ZIP member forbidden: {name}")
        if info.flag_bits & 0x1:
            raise ValueError(f"encrypted ZIP member forbidden: {name}")
        if info.file_size > MAX_MEMBER_BYTES:
            raise ValueError(f"source archive member exceeds safety limit: {name}")
        total += info.file_size
        if total > MAX_TOTAL_BYTES:
            raise ValueError("source archive exceeds uncompressed safety limit")
    return infos


def safe_extract(archive: zipfile.ZipFile, destination: Path) -> None:
    """Extract regular files only, after validating every member and boundary."""
    destination = destination.resolve()
    destination.mkdir(parents=True, exist_ok=True)
    infos = validated_members(archive)
    for info in infos:
        relative = _validated_portable_path(info.filename)
        target = destination.joinpath(*relative.parts)
        resolved_parent = target.parent.resolve()
        if destination != resolved_parent and destination not in resolved_parent.parents:
            raise ValueError(f"archive member escapes destination: {relative}")
        target.parent.mkdir(parents=True, exist_ok=True)
        data = archive.read(info)
        if len(data) != info.file_size:
            raise ValueError(f"ZIP member size mismatch while extracting: {relative}")
        target.write_bytes(data)
        mode = (info.external_attr >> 16) & 0o777
        if mode:
            os.chmod(target, mode & 0o755)
