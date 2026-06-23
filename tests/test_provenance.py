from __future__ import annotations

import json
import unittest
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]


class ProvenanceSchemaTests(unittest.TestCase):
    def test_schema_accepts_minimal_statement_shape(self) -> None:
        schema = json.loads((ROOT / "schemas/provenance.schema.json").read_text())
        statement = {
            "_type": "https://in-toto.io/Statement/v1",
            "subject": [
                {"name": f"artifact-{index}", "digest": {"sha256": "0" * 64}}
                for index in range(4)
            ],
            "predicateType": "https://slsa.dev/provenance/v1",
            "predicate": {
                "buildDefinition": {
                    "buildType": "https://example.org/build",
                    "externalParameters": {},
                    "internalParameters": {},
                    "resolvedDependencies": [{}, {}, {}, {}],
                },
                "runDetails": {
                    "builder": {"id": "https://example.org/builder"},
                    "metadata": {},
                },
            },
        }
        jsonschema.Draft202012Validator(schema).validate(statement)


if __name__ == "__main__":
    unittest.main()
