from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

from check_references import validate  # noqa: E402


class ReferenceAuditTests(unittest.TestCase):
    def test_repository_references_are_consistent(self) -> None:
        self.assertEqual(validate(ROOT), [])

    def test_missing_doi_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / 'repo'
            shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns('.git', '.lake', 'site', 'release', 'docs/generated', '__pycache__'))
            rendered = copy / 'docs' / 'paper' / 'references.md'
            rendered.write_text(
                rendered.read_text(encoding='utf-8').replace(
                    'https://doi.org/10.1007/BF01211762', 'https://example.invalid/removed', 1
                ),
                encoding='utf-8',
            )
            self.assertTrue(any('missing DOI' in error for error in validate(copy)))


if __name__ == '__main__':
    unittest.main()
