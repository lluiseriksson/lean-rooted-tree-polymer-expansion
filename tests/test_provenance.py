from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from generate_provenance import build_statement  # noqa: E402
from project_config import load_project  # noqa: E402


class ProvenanceSchemaTests(unittest.TestCase):
    def setUp(self) -> None:
        self.project = load_project(ROOT)
        self.schema = json.loads(
            (ROOT / "schemas/provenance.schema.json").read_text(encoding="utf-8")
        )
        self.source_inputs = {
            "python_lock": ROOT / self.project["python_lock"],
            "theorem_manifest": ROOT / "archive/theorem-manifest.json",
            "proof_dag": ROOT / self.project["proof_dag"],
            "paper_manifest": ROOT / "docs/paper/manifest.json",
            "actions_manifest": ROOT / "archive/actions-manifest.json",
            "citation_schema": ROOT / self.project["citation_schema"],
            "source_manifest": ROOT / "MANIFEST.sha256",
        }

    def _statement(self) -> dict[str, object]:
        with tempfile.TemporaryDirectory() as temp:
            subjects = []
            for index in range(4):
                path = Path(temp) / f"artifact-{index}"
                path.write_bytes(f"artifact {index}\n".encode())
                subjects.append(path)
            return build_statement(self.project, subjects, self.source_inputs)

    def test_schema_accepts_generated_statement(self) -> None:
        jsonschema.Draft202012Validator(self.schema).validate(self._statement())

    def test_schema_rejects_false_hosted_execution_claim(self) -> None:
        statement = copy.deepcopy(self._statement())
        statement["predicate"]["runDetails"]["metadata"]["executionBound"] = True  # type: ignore[index]
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.Draft202012Validator(self.schema).validate(statement)

    def test_deterministic_statement_does_not_claim_hosted_execution(self) -> None:
        statement = self._statement()
        predicate = statement["predicate"]
        assert isinstance(predicate, dict)
        run_details = predicate["runDetails"]
        assert isinstance(run_details, dict)
        metadata = run_details["metadata"]
        assert isinstance(metadata, dict)
        self.assertIs(metadata["executionBound"], False)
        self.assertIs(metadata["hostedAttestationRequired"], True)
        builder = run_details["builder"]
        assert isinstance(builder, dict)
        self.assertIn("deterministic-source-tooling-v1", builder["id"])
        self.assertNotIn("actions/workflows/release", builder["id"])

        definition = predicate["buildDefinition"]
        assert isinstance(definition, dict)
        internal = definition["internalParameters"]
        assert isinstance(internal, dict)
        self.assertEqual(internal["releaseRecipe"], ["make package-determinism"])
        self.assertIn("make lean-oracle", internal["requiredExternalGates"])


if __name__ == "__main__":
    unittest.main()
