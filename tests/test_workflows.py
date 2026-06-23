from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from check_workflows import validate  # noqa: E402

COPY_IGNORE = shutil.ignore_patterns(
    ".git",
    ".lake",
    "site",
    "release",
    ".venv*",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
)


class WorkflowAuditTests(unittest.TestCase):
    def _copy_repo(self, parent: str) -> Path:
        copy = Path(parent) / "repo"
        shutil.copytree(ROOT, copy, ignore=COPY_IGNORE)
        return copy

    def test_repository_workflows_pass(self) -> None:
        self.assertEqual(validate(ROOT), [])

    def test_unmanifested_action_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copy = self._copy_repo(tmp)
            ci = copy / ".github" / "workflows" / "ci.yml"
            ci.write_text(
                ci.read_text(encoding="utf-8") + "\n# uses: example/untrusted@v1\n",
                encoding="utf-8",
            )
            self.assertTrue(
                any("missing from actions manifest" in error for error in validate(copy))
            )

    def test_manifest_ref_drift_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copy = self._copy_repo(tmp)
            manifest_path = copy / "archive" / "actions-manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["actions"]["actions/checkout"] = "0" * 40
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            self.assertTrue(any("action ref mismatch" in error for error in validate(copy)))

    def test_mutable_workflow_ref_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copy = self._copy_repo(tmp)
            ci = copy / ".github" / "workflows" / "ci.yml"
            text = ci.read_text(encoding="utf-8")
            manifest = json.loads(
                (copy / "archive" / "actions-manifest.json").read_text(
                    encoding="utf-8"
                )
            )
            sha = manifest["actions"]["actions/checkout"]
            ci.write_text(
                text.replace(f"actions/checkout@{sha}", "actions/checkout@v4", 1),
                encoding="utf-8",
            )
            self.assertTrue(
                any("not a full immutable SHA" in error for error in validate(copy))
            )

    def test_lean_action_autoconfig_drift_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copy = self._copy_repo(tmp)
            ci = copy / ".github" / "workflows" / "ci.yml"
            text = ci.read_text(encoding="utf-8")
            ci.write_text(
                text.replace("auto-config: false", "auto-config: true", 1),
                encoding="utf-8",
            )
            self.assertTrue(
                any("lean-action missing explicit policy" in error for error in validate(copy))
            )

    def test_leanchecker_policy_drift_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copy = self._copy_repo(tmp)
            ci = copy / ".github" / "workflows" / "ci.yml"
            text = ci.read_text(encoding="utf-8")
            ci.write_text(
                text.replace("leanchecker: true", "leanchecker: false", 1),
                encoding="utf-8",
            )
            self.assertTrue(
                any("lean-action missing explicit policy" in error for error in validate(copy))
            )

    def test_duplicate_lean_build_gate_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copy = self._copy_repo(tmp)
            ci = copy / ".github" / "workflows" / "ci.yml"
            text = ci.read_text(encoding="utf-8")
            ci.write_text(
                text.replace("run: make lean-oracle", "run: make lean", 1),
                encoding="utf-8",
            )
            self.assertTrue(
                any("second full Lean build" in error for error in validate(copy))
            )

    def test_release_permissions_cannot_be_workflow_wide(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copy = self._copy_repo(tmp)
            path = copy / ".github" / "workflows" / "release.yml"
            text = path.read_text(encoding="utf-8")
            path.write_text(
                text.replace("  contents: read", "  contents: write", 1),
                encoding="utf-8",
            )
            errors = validate(copy)
            self.assertTrue(
                any(
                    "default to read-only" in error or "workflow-wide" in error
                    for error in errors
                )
            )

    def test_release_publish_glob_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copy = self._copy_repo(tmp)
            path = copy / ".github" / "workflows" / "release.yml"
            text = path.read_text(encoding="utf-8")
            path.write_text(
                text.replace(
                    '"release/${RELEASE_STEM}.zip"', '"release/*.zip"', 1
                ),
                encoding="utf-8",
            )
            self.assertTrue(
                any("broad release asset globs" in error for error in validate(copy))
            )

    def test_release_publish_job_cannot_checkout_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copy = self._copy_repo(tmp)
            path = copy / ".github" / "workflows" / "release.yml"
            text = path.read_text(encoding="utf-8")
            marker = "  publish:\n"
            prefix, publish = text.split(marker, 1)
            publish = publish.replace(
                "    steps:\n",
                "    steps:\n"
                "      - uses: actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5\n"
                "        with:\n"
                "          persist-credentials: false\n",
                1,
            )
            path.write_text(prefix + marker + publish, encoding="utf-8")
            self.assertTrue(any("must not checkout" in error for error in validate(copy)))

    def test_release_publish_job_cannot_execute_repository_scripts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copy = self._copy_repo(tmp)
            path = copy / ".github" / "workflows" / "release.yml"
            text = path.read_text(encoding="utf-8")
            marker = "  publish:\n"
            prefix, publish = text.split(marker, 1)
            publish = publish.replace(
                "    steps:\n",
                "    steps:\n"
                "      - name: Unsafe source execution\n"
                "        run: python scripts/verify_release.py\n",
                1,
            )
            path.write_text(prefix + marker + publish, encoding="utf-8")
            self.assertTrue(
                any(
                    "must not execute repository build scripts" in error
                    for error in validate(copy)
                )
            )

    def test_release_publish_job_must_bind_index_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copy = self._copy_repo(tmp)
            path = copy / ".github" / "workflows" / "release.yml"
            text = path.read_text(encoding="utf-8")
            path.write_text(
                text.replace(
                    "release index artifact metadata mismatch",
                    "release index artifact mismatch",
                    1,
                ),
                encoding="utf-8",
            )
            self.assertTrue(
                any("bind release-index metadata" in error for error in validate(copy))
            )


if __name__ == "__main__":
    unittest.main()
