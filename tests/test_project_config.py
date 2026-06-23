from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from project_config import (  # noqa: E402
    load_project,
    release_stem,
    repository_full_name,
    repository_url,
    site_url,
)


class ProjectConfigTests(unittest.TestCase):
    def test_current_identity(self) -> None:
        project = load_project(ROOT)
        self.assertEqual(repository_full_name(project), "lluiseriksson/lean-rooted-tree-polymer-expansion")
        self.assertEqual(repository_url(project), "https://github.com/lluiseriksson/lean-rooted-tree-polymer-expansion")
        self.assertEqual(site_url(project), "https://lluiseriksson.github.io/lean-rooted-tree-polymer-expansion/")
        self.assertEqual(release_stem(project), "lean-rooted-tree-polymer-expansion-v2.4.2")

    def test_missing_required_field_is_rejected(self) -> None:
        project = load_project(ROOT)
        project.pop("upstream_commit")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "project.json"
            path.write_text(json.dumps(project), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_project(Path(tmp))

    def test_schema_version_and_adopted_identity(self) -> None:
        project = load_project(ROOT)
        self.assertEqual(project["schema_version"], 4)
        self.assertEqual(project["rename_status"], "adopted")
        self.assertEqual(project["repository_slug"], project["recommended_repository_slug"])


if __name__ == "__main__":
    unittest.main()
