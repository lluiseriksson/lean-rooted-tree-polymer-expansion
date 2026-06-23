from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from check_accessibility import validate_file  # noqa: E402


class AccessibilityTests(unittest.TestCase):
    def test_empty_image_alt_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "page.md"
            path.write_text("# Title\n\n![](image.png)\n", encoding="utf-8")
            self.assertTrue(any("empty alt" in error for error in validate_file(path)))

    def test_heading_jump_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "page.md"
            path.write_text("# Title\n\n### Jump\n", encoding="utf-8")
            self.assertTrue(any("jumps" in error for error in validate_file(path)))

    def test_fenced_headings_are_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "page.md"
            path.write_text("# Title\n\n```markdown\n### Example\n```\n", encoding="utf-8")
            self.assertEqual(validate_file(path), [])


if __name__ == "__main__":
    unittest.main()
