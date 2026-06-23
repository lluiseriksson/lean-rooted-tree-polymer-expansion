from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

from check_workflows import validate  # noqa: E402


class WorkflowAuditTests(unittest.TestCase):
    def test_repository_workflows_pass(self) -> None:
        self.assertEqual(validate(ROOT), [])

    def test_unmanifested_action_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / 'repo'
            shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns('.git', '.lake', 'site', 'release', '.venv*', '__pycache__', '.pytest_cache', '.mypy_cache'))
            ci = copy / '.github' / 'workflows' / 'ci.yml'
            ci.write_text(ci.read_text(encoding='utf-8') + '\n# uses: example/untrusted@v1\n', encoding='utf-8')
            self.assertTrue(any('missing from actions manifest' in error for error in validate(copy)))

    def test_manifest_ref_drift_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / 'repo'
            shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns('.git', '.lake', 'site', 'release', '.venv*', '__pycache__', '.pytest_cache', '.mypy_cache'))
            manifest_path = copy / 'archive' / 'actions-manifest.json'
            manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
            manifest['actions']['actions/checkout'] = '0' * 40
            manifest_path.write_text(json.dumps(manifest), encoding='utf-8')
            self.assertTrue(any('action ref mismatch' in error for error in validate(copy)))

    def test_mutable_workflow_ref_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / 'repo'
            shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns('.git', '.lake', 'site', 'release', '.venv*', '__pycache__', '.pytest_cache', '.mypy_cache'))
            ci = copy / '.github' / 'workflows' / 'ci.yml'
            text = ci.read_text(encoding='utf-8')
            manifest = json.loads((copy / 'archive' / 'actions-manifest.json').read_text(encoding='utf-8'))
            sha = manifest['actions']['actions/checkout']
            ci.write_text(text.replace(f'actions/checkout@{sha}', 'actions/checkout@v4', 1), encoding='utf-8')
            self.assertTrue(any('not a full immutable SHA' in error for error in validate(copy)))

    def test_lean_action_autoconfig_drift_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / 'repo'
            shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns('.git', '.lake', 'site', 'release', '.venv*', '__pycache__', '.pytest_cache', '.mypy_cache'))
            ci = copy / '.github' / 'workflows' / 'ci.yml'
            text = ci.read_text(encoding='utf-8')
            ci.write_text(text.replace('auto-config: false', 'auto-config: true', 1), encoding='utf-8')
            self.assertTrue(any('lean-action missing explicit policy' in error for error in validate(copy)))

    def test_leanchecker_policy_drift_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / 'repo'
            shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns('.git', '.lake', 'site', 'release', '.venv*', '__pycache__', '.pytest_cache', '.mypy_cache'))
            ci = copy / '.github' / 'workflows' / 'ci.yml'
            text = ci.read_text(encoding='utf-8')
            ci.write_text(text.replace('leanchecker: true', 'leanchecker: false', 1), encoding='utf-8')
            self.assertTrue(any('lean-action missing explicit policy' in error for error in validate(copy)))

    def test_duplicate_lean_build_gate_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / 'repo'
            shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns('.git', '.lake', 'site', 'release', '.venv*', '__pycache__', '.pytest_cache', '.mypy_cache'))
            ci = copy / '.github' / 'workflows' / 'ci.yml'
            text = ci.read_text(encoding='utf-8')
            ci.write_text(text.replace('run: make lean-oracle', 'run: make lean', 1), encoding='utf-8')
            self.assertTrue(any('second full Lean build' in error for error in validate(copy)))


if __name__ == '__main__':
    unittest.main()
