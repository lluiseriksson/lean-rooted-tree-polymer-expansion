from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]


class CitationSchemaTests(unittest.TestCase):
    def setUp(self) -> None:
        self.schema = json.loads((ROOT / "schemas/citation-cff.schema.json").read_text())
        self.citation = yaml.safe_load((ROOT / "CITATION.cff").read_text())
        self.citation["date-released"] = str(self.citation["date-released"])

    def test_repository_citation_validates(self) -> None:
        jsonschema.Draft202012Validator(self.schema).validate(self.citation)

    def test_missing_license_is_rejected(self) -> None:
        bad = copy.deepcopy(self.citation)
        bad.pop("license")
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.Draft202012Validator(self.schema).validate(bad)


if __name__ == "__main__":
    unittest.main()
