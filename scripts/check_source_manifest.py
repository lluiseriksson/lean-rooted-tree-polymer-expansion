#!/usr/bin/env python3
"""Fail when MANIFEST.sha256 does not describe the committed source tree."""
from __future__ import annotations

from project_config import ROOT
from source_inventory import SourceInventoryError, verify_manifest


def main() -> None:
    try:
        count = verify_manifest(ROOT)
    except SourceInventoryError as exc:
        raise SystemExit(f"source manifest audit failed:\n{exc}") from exc
    print(f"source manifest audit: OK ({count} entries)")


if __name__ == "__main__":
    main()
