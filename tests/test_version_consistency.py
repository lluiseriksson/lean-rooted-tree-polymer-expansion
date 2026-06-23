from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from check_version_consistency import validate


class VersionConsistencyTests(unittest.TestCase):
    def test_repository_versions_are_consistent(self) -> None:
        self.assertEqual(validate(ROOT), [])

    def test_project_drift_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            copy = Path(temp) / "repo"
            shutil.copytree(
                ROOT,
                copy,
                ignore=shutil.ignore_patterns(
                    ".git", ".lake", "site", "release", ".venv*",
                    "__pycache__", ".pytest_cache", ".mypy_cache"
                ),
            )
            path = copy / "codemeta.json"
            data = json.loads(path.read_text())
            data["version"] = "9.9.9"
            path.write_text(json.dumps(data))
            self.assertTrue(any("codemeta" in error for error in validate(copy)))

    def test_release_playbook_cli_drift_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            copy = Path(temp) / "repo"
            shutil.copytree(
                ROOT,
                copy,
                ignore=shutil.ignore_patterns(
                    ".git", ".lake", "site", "release", ".venv*",
                    "__pycache__", ".pytest_cache", ".mypy_cache"
                ),
            )
            path = copy / "docs/maintainers/release-playbook.md"
            text = path.read_text(encoding="utf-8").replace(" --date ", " ", 1)
            path.write_text(text, encoding="utf-8")
            self.assertTrue(any("bump_version.py --date" in error for error in validate(copy)))


if __name__ == "__main__":
    unittest.main()
