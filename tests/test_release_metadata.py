from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from generate_cyclonedx import locked_python_requirements, purl_for_git  # noqa: E402
from rename_repository import valid_slug  # noqa: E402


class ReleaseMetadataTests(unittest.TestCase):
    def test_github_purl(self) -> None:
        self.assertEqual(
            purl_for_git("mathlib", "https://github.com/leanprover-community/mathlib4.git", "abc123"),
            "pkg:github/leanprover-community/mathlib4@abc123",
        )

    def test_generic_purl_fallback(self) -> None:
        self.assertEqual(
            purl_for_git("library", "https://example.org/library.git", "deadbeef"),
            "pkg:generic/library@deadbeef",
        )

    def test_documentation_requirements_are_exactly_pinned(self) -> None:
        requirements = locked_python_requirements(ROOT)
        self.assertGreaterEqual(len(requirements), 4)
        self.assertEqual(len(requirements), len({name.lower() for name, _ in requirements}))
        self.assertTrue(all(version for _, version in requirements))

    def test_repository_slug_validation(self) -> None:
        self.assertTrue(valid_slug("lean-rooted-tree-polymer-expansion"))
        self.assertFalse(valid_slug("Lean Rooted Tree"))
        self.assertFalse(valid_slug("-bad"))


if __name__ == "__main__":
    unittest.main()
