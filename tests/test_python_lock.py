from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from python_requirements import canonical_name, parse_exact_requirements  # noqa: E402


class PythonRequirementsTests(unittest.TestCase):
    def test_canonical_name(self) -> None:
        self.assertEqual(canonical_name("PyYAML"), "pyyaml")
        self.assertEqual(canonical_name("jsonschema_specifications"), "jsonschema-specifications")

    def test_exact_parser_rejects_ranges(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "requirements.txt"
            path.write_text("mkdocs>=1.6\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                parse_exact_requirements(path)

    def test_exact_parser_rejects_canonical_duplicates(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "requirements.txt"
            path.write_text("PyYAML==6.0.3\npyyaml==6.0.3\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                parse_exact_requirements(path)


if __name__ == "__main__":
    unittest.main()
