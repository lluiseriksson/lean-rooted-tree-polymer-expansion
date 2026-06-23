from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from project_config import load_project  # noqa: E402
from release_inventory import (  # noqa: E402
    CORE_ARTIFACT_SPECS,
    aggregate_path,
    checksum_subject_paths,
    expected_release_names,
    render_aggregate,
    sidecar_path,
    verify_release_inventory,
    write_sidecar,
)


class ReleaseInventoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.project = load_project(ROOT)

    def _valid_release(self, directory: Path) -> tuple[Path, ...]:
        directory.mkdir()
        subjects = checksum_subject_paths(self.project, directory)
        for index, path in enumerate(subjects):
            path.write_bytes(f"artifact-{index}\n".encode("utf-8"))
            write_sidecar(path)
        aggregate_path(self.project, directory).write_bytes(render_aggregate(subjects))
        return subjects

    def test_expected_inventory_is_unique_and_complete(self) -> None:
        names = expected_release_names(self.project)
        self.assertEqual(len(names), 13)
        self.assertEqual(len(names), len(set(names)))
        self.assertTrue(names[-1].endswith(".checksums.sha256"))

    def test_indexed_artifact_metadata_is_canonical(self) -> None:
        self.assertEqual(
            [
                (spec.suffix, spec.role, spec.media_type)
                for spec in CORE_ARTIFACT_SPECS
            ],
            [
                (".zip", "source-archive", "application/zip"),
                (".spdx.json", "spdx-sbom", "application/spdx+json"),
                (
                    ".cdx.json",
                    "cyclonedx-sbom",
                    "application/vnd.cyclonedx+json",
                ),
                (".buildinfo.json", "build-information", "application/json"),
                (
                    ".intoto.jsonl",
                    "in-toto-provenance",
                    "application/jsonl",
                ),
            ],
        )

    def test_valid_exact_inventory_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            release = Path(tmp) / "release"
            self._valid_release(release)
            paths = verify_release_inventory(self.project, release)
            self.assertEqual(
                {path.name for path in paths},
                set(expected_release_names(self.project)),
            )

    def test_unexpected_asset_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            release = Path(tmp) / "release"
            self._valid_release(release)
            (release / "stale.zip").write_bytes(b"stale")
            with self.assertRaisesRegex(ValueError, "unexpected: stale.zip"):
                verify_release_inventory(self.project, release)

    def test_noncanonical_sidecar_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            release = Path(tmp) / "release"
            subjects = self._valid_release(release)
            sidecar_path(subjects[0]).write_text(
                sidecar_path(subjects[0]).read_text(encoding="utf-8") + "\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "non-canonical checksum sidecar"):
                verify_release_inventory(self.project, release)

    def test_reordered_aggregate_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            release = Path(tmp) / "release"
            subjects = self._valid_release(release)
            aggregate_path(self.project, release).write_bytes(
                render_aggregate(reversed(subjects))
            )
            with self.assertRaisesRegex(ValueError, "non-canonical aggregate checksum"):
                verify_release_inventory(self.project, release)

    def test_directory_in_release_set_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            release = Path(tmp) / "release"
            self._valid_release(release)
            (release / "unexpected-directory").mkdir()
            with self.assertRaisesRegex(ValueError, "non-regular entries"):
                verify_release_inventory(self.project, release)


if __name__ == "__main__":
    unittest.main()
