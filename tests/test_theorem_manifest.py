from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from check_theorem_manifest import validate  # noqa: E402


class TheoremManifestTests(unittest.TestCase):
    def test_repository_manifest_is_consistent(self) -> None:
        self.assertEqual(validate(ROOT), [])

    def test_version_drift_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / "repo"
            shutil.copytree(
                ROOT,
                copy,
                ignore=shutil.ignore_patterns(
                    ".git", ".lake", "site", "release", "docs/generated", "__pycache__"
                ),
            )
            manifest_path = copy / "archive" / "theorem-manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["version"] = "0.0.0"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            errors = validate(copy)
            self.assertTrue(any("version" in error for error in errors))

    def test_signature_drift_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / "repo"
            shutil.copytree(
                ROOT,
                copy,
                ignore=shutil.ignore_patterns(
                    ".git", ".lake", "site", "release", "docs/generated", "__pycache__"
                ),
            )
            wrapper = copy / "MarkedRootedClosure" / "PaperTheorems.lean"
            wrapper.write_text(
                wrapper.read_text(encoding="utf-8").replace(
                    "(n : ℕ) :", "(n : ℕ) (extra : True) :", 1
                ),
                encoding="utf-8",
            )
            errors = validate(copy)
            self.assertTrue(any("signature hash mismatch" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
