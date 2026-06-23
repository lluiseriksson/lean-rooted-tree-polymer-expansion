from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from assemble_paper import demote_headings, rewrite_paper_relative_links  # noqa: E402


class AssemblePaperTests(unittest.TestCase):
    def test_demotes_headings_outside_fences(self) -> None:
        source = "# Title\n\n## Section\n\n```lean\n#check Nat\n```\n"
        result = demote_headings(source)
        self.assertIn("## Title", result)
        self.assertIn("### Section", result)
        self.assertIn("#check Nat", result)
        self.assertNotIn("##check Nat", result)

    def test_rewrites_sibling_links(self) -> None:
        source = "[Next](02-polymer-systems.md) and [anchor](#local)."
        result = rewrite_paper_relative_links(source)
        self.assertIn("../paper/02-polymer-systems.md", result)
        self.assertIn("[anchor](#local)", result)

    def test_preserves_external_links_and_parent_images(self) -> None:
        source = "[External](https://example.org) ![Figure](../assets/images/proof-pipeline.png)"
        self.assertEqual(rewrite_paper_relative_links(source), source)


if __name__ == "__main__":
    unittest.main()
