from __future__ import annotations

import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from archive_safety import safe_extract  # noqa: E402


class ArchiveSafetyTests(unittest.TestCase):
    def test_valid_archive_extracts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "valid.zip"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("release/README.md", "ok")
            out = root / "out"
            with zipfile.ZipFile(path) as archive:
                safe_extract(archive, out)
            self.assertEqual((out / "release/README.md").read_text(), "ok")

    def test_traversal_is_rejected_before_extraction(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "bad.zip"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("release/../escape", "bad")
            with zipfile.ZipFile(path) as archive:
                with self.assertRaisesRegex(ValueError, "unsafe archive path"):
                    safe_extract(archive, root / "out")
            self.assertFalse((root / "escape").exists())


if __name__ == "__main__":
    unittest.main()
