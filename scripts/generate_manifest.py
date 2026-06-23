#!/usr/bin/env python3
"""Regenerate the canonical source-tree SHA-256 manifest."""
from __future__ import annotations

from project_config import ROOT
from source_inventory import MANIFEST_REL, write_manifest


def main() -> None:
    count = write_manifest(ROOT)
    print(f"wrote {MANIFEST_REL.as_posix()} with {count} entries")


if __name__ == "__main__":
    main()
