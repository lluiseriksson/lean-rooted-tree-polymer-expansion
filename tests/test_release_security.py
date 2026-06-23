from __future__ import annotations

import hashlib
import sys
import tempfile
import unittest
import warnings
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

from project_config import load_project, release_stem  # noqa: E402
from verify_release import verify_zip  # noqa: E402


class ReleaseSecurityTests(unittest.TestCase):
    def _write_sidecar(self, path: Path) -> None:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        path.with_suffix(path.suffix + '.sha256').write_bytes(
            f'{digest}  {path.name}\n'.encode('utf-8')
        )

    def test_path_traversal_is_rejected(self) -> None:
        project = load_project(ROOT)
        stem = release_stem(project)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / f'{stem}.zip'
            with zipfile.ZipFile(path, 'w') as archive:
                archive.writestr(f'{stem}/../escape.txt', b'bad')
            self._write_sidecar(path)
            with self.assertRaisesRegex(ValueError, 'unsafe archive path'):
                verify_zip(path, project)

    def test_case_insensitive_collision_is_rejected(self) -> None:
        project = load_project(ROOT)
        stem = release_stem(project)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / f'{stem}.zip'
            with zipfile.ZipFile(path, 'w') as archive:
                archive.writestr(f'{stem}/README.md', b'a')
                archive.writestr(f'{stem}/readme.md', b'b')
            self._write_sidecar(path)
            with self.assertRaisesRegex(ValueError, 'case-insensitive collision'):
                verify_zip(path, project)

    def test_duplicate_member_is_rejected(self) -> None:
        project = load_project(ROOT)
        stem = release_stem(project)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / f'{stem}.zip'
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', UserWarning)
                with zipfile.ZipFile(path, 'w') as archive:
                    archive.writestr(f'{stem}/README.md', b'a')
                    archive.writestr(f'{stem}/README.md', b'b')
            self._write_sidecar(path)
            with self.assertRaisesRegex(ValueError, 'duplicate ZIP member'):
                verify_zip(path, project)


if __name__ == '__main__':
    unittest.main()
