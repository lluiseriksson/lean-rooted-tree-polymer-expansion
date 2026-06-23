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


def validated_members(archive: zipfile.ZipFile) -> list[zipfile.ZipInfo]:
    infos = [info for info in archive.infolist() if not info.is_dir()]
    names = [info.filename for info in infos]
    if len(names) != len(set(names)):
        raise ValueError("duplicate ZIP member name")
    normalised = [unicodedata.normalize("NFC", name) for name in names]
    if len(normalised) != len(set(normalised)):
        raise ValueError("Unicode-normalization collision in ZIP member names")
    folded = [name.casefold() for name in normalised]
    if len(folded) != len(set(folded)):
        raise ValueError("case-insensitive collision in ZIP member names")
    total = 0
    for info, raw_name in zip(infos, normalised):
        name = PurePosixPath(raw_name)
        if name.is_absolute() or ".." in name.parts or "\\" in raw_name or "\x00" in raw_name:
            raise ValueError(f"unsafe archive path: {name}")
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
        relative = PurePosixPath(unicodedata.normalize("NFC", info.filename))
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
