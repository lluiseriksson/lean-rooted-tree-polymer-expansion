from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from source_inventory import (  # noqa: E402
    SourceInventoryError,
    collect_source_files,
    verify_manifest,
    write_manifest,
)


class SourceInventoryTests(unittest.TestCase):
    def test_repository_manifest_is_current(self) -> None:
        self.assertGreater(verify_manifest(ROOT), 100)

    def test_content_drift_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source.txt"
            source.write_text("before\n", encoding="utf-8")
            write_manifest(root)
            source.write_text("after\n", encoding="utf-8")
            with self.assertRaisesRegex(SourceInventoryError, "manifest is stale"):
                verify_manifest(root)

    def test_unlisted_file_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "first.txt").write_text("first\n", encoding="utf-8")
            write_manifest(root)
            (root / "second.txt").write_text("second\n", encoding="utf-8")
            with self.assertRaisesRegex(SourceInventoryError, "manifest is stale"):
                verify_manifest(root)

    def test_generated_and_build_outputs_are_excluded(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "kept.txt").write_text("kept\n", encoding="utf-8")
            generated = root / "docs" / "generated"
            generated.mkdir(parents=True)
            (generated / "article.md").write_text("generated\n", encoding="utf-8")
            release = root / "release"
            release.mkdir()
            (release / "artifact.zip").write_bytes(b"ignored")
            (root / ".oracle.log").write_text(
                "partial oracle output\n", encoding="utf-8"
            )
            write_manifest(root)
            self.assertEqual(verify_manifest(root), 1)

    def test_case_insensitive_collision_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            upper = root / "README.md"
            lower = root / "readme.md"
            upper.write_text("upper\n", encoding="utf-8")
            if lower.exists():
                self.skipTest("case-insensitive filesystem prevents collision fixture")
            lower.write_text("lower\n", encoding="utf-8")
            with self.assertRaisesRegex(SourceInventoryError, "portable source-path collision"):
                collect_source_files(root)

    def test_case_insensitive_directory_collision_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            upper = root / "Sources"
            lower = root / "sources"
            upper.mkdir()
            if lower.exists():
                self.skipTest("case-insensitive filesystem prevents collision fixture")
            lower.mkdir()
            (upper / "first.txt").write_text("first\n", encoding="utf-8")
            (lower / "second.txt").write_text("second\n", encoding="utf-8")
            with self.assertRaisesRegex(SourceInventoryError, "portable source-path collision"):
                collect_source_files(root)

    def test_windows_device_name_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "NUL.txt").write_text("bad\n", encoding="utf-8")
            with self.assertRaisesRegex(SourceInventoryError, "non-portable source path"):
                collect_source_files(root)

    @unittest.skipIf(os.name == "nt", "symlink creation semantics differ on Windows")
    def test_source_symlink_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "target.txt"
            target.write_text("target\n", encoding="utf-8")
            (root / "alias.txt").symlink_to(target)
            with self.assertRaisesRegex(SourceInventoryError, "symlink is forbidden"):
                collect_source_files(root)

    @unittest.skipIf(os.name == "nt", "symlink creation semantics differ on Windows")
    def test_source_directory_symlink_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "target"
            target.mkdir()
            (target / "inside.txt").write_text("target\n", encoding="utf-8")
            (root / "alias").symlink_to(target, target_is_directory=True)
            with self.assertRaisesRegex(SourceInventoryError, "symlink is forbidden"):
                collect_source_files(root)


if __name__ == "__main__":
    unittest.main()
