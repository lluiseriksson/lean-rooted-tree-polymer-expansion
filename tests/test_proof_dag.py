from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from check_proof_dag import validate


class ProofDagTests(unittest.TestCase):
    def test_repository_proof_dag_is_current(self) -> None:
        self.assertEqual(validate(ROOT), [])

    def test_cycle_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            copy = Path(temp) / "repo"
            import shutil
            shutil.copytree(
                ROOT,
                copy,
                ignore=shutil.ignore_patterns(
                    ".git", ".lake", "site", "release", ".venv*",
                    "__pycache__", ".pytest_cache", ".mypy_cache"
                ),
            )
            path = copy / "archive/proof-dag.json"
            data = json.loads(path.read_text())
            data["edges"].append({
                "from": "public.target-preserving",
                "to": "upstream.rooted-profile",
                "relation": "combinatorial-input",
            })
            path.write_text(json.dumps(data))
            self.assertTrue(any("cycle" in error for error in validate(copy)))


if __name__ == "__main__":
    unittest.main()
