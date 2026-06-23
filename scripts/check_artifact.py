#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

from project_config import ROOT, load_project

project = load_project()
version = project["version"]
upstream = project["upstream_commit"]

required = [
    "README.md",
    "project.json",
    "REPOSITORY_HISTORY.md",
    "AGENTS.md",
    "GOVERNANCE.md",
    "SUPPORT.md",
    "MIGRATION.md",
    "LICENSE",
    "NOTICE",
    "CITATION.cff",
    "CITATION.bib",
    "codemeta.json",
    ".zenodo.json",
    "lakefile.lean",
    "lake-manifest.json",
    "lean-toolchain",
    "MarkedRootedClosure.lean",
    "MarkedRootedClosure/PaperTheorems.lean",
    "MarkedRootedClosure/Oracle.lean",
    "mkdocs.yml",
    "requirements-docs.txt",
    "requirements-docs.lock",
    "schemas/citation-cff.schema.json",
    "schemas/proof-dag.schema.json",
    "schemas/provenance.schema.json",
    "schemas/project.schema.json",
    "schemas/theorem-manifest.schema.json",
    "schemas/paper-manifest.schema.json",
    "schemas/buildinfo.schema.json",
    "schemas/release-index.schema.json",
    "schemas/actions-manifest.schema.json",
    "docs/index.md",
    "docs/about/overview.md",
    "docs/about/claims.md",
    "docs/about/notation.md",
    "docs/about/citation.md",
    "docs/about/machine-readable.md",
    "docs/llms.txt",
    "docs/formalization/index.md",
    "docs/paper/index.md",
    "docs/paper/manifest.json",
    "docs/paper/00-reader-guide.md",
    "docs/paper/01-introduction.md",
    "docs/paper/07-target-preserving-decay.md",
    "docs/paper/11-limitations.md",
    "docs/paper/references.md",
    "docs/paper/references.bib",
    "docs/publication/author-declarations.md",
    "docs/publication/submission-metadata.md",
    "docs/publication/submission-metadata.yaml",
    "docs/assets/source/graphical-abstract.tex",
    "docs/assets/stylesheets/print.css",
    "docs/artifact/theorem-map.md",
    "docs/artifact/proof-dependency-graph.md",
    "docs/artifact/source-provenance.md",
    "docs/artifact/reproducibility.md",
    "docs/artifact/verification-contract.md",
    "docs/artifact/release-evidence.md",
    "docs/maintainers/repository-history.md",
    "docs/maintainers/release-playbook.md",
    "docs/assets/images/proof-pipeline.png",
    "archive/UPSTREAM.lock",
    "archive/theorem-manifest.json",
    "archive/proof-dag.json",
    "archive/actions-manifest.json",
    ".github/workflows/ci.yml",
    ".github/workflows/pages.yml",
    ".github/workflows/release.yml",
    ".github/workflows/dependency-review.yml",
    ".github/workflows/maintenance.yml",
    "scripts/assemble_paper.py",
    "scripts/check_paper_manifest.py",
    "scripts/check_lake_lock.py",
    "scripts/check_project_identity.py",
    "scripts/check_theorem_manifest.py",
    "scripts/check_version_consistency.py",
    "scripts/check_python_lock.py",
    "scripts/check_source_manifest.py",
    "scripts/source_inventory.py",
    "scripts/check_proof_dag.py",
    "scripts/check_accessibility.py",
    "scripts/lean_signatures.py",
    "scripts/check_references.py",
    "scripts/check_agent_index.py",
    "scripts/check_workflows.py",
    "scripts/rename_repository.py",
    "scripts/generate_sbom.py",
    "scripts/generate_cyclonedx.py",
    "scripts/generate_buildinfo.py",
    "scripts/generate_release_index.py",
    "scripts/generate_provenance.py",
    "scripts/archive_safety.py",
    "scripts/process_runner.py",
    "scripts/run_lean_gate.py",
    "scripts/check_release_determinism.py",
    "scripts/smoke_test_release.py",
    "scripts/cleanroom_audit.py",
    "scripts/verify_release.py",
    "tests/test_project_config.py",
    "tests/test_assemble_paper.py",
    "tests/test_release_metadata.py",
    "tests/test_theorem_manifest.py",
    "tests/test_lean_signatures.py",
    "tests/test_oracle_output.py",
    "tests/test_references.py",
    "tests/test_workflows.py",
    "tests/test_agent_index.py",
    "tests/test_release_security.py",
    "tests/test_archive_safety.py",
    "tests/test_accessibility.py",
    "tests/test_metadata_schema.py",
    "tests/test_proof_dag.py",
    "tests/test_process_runner.py",
    "tests/test_provenance.py",
    "tests/test_run_lean_gate.py",
    "tests/test_python_lock.py",
    "tests/test_source_inventory.py",
    "tests/test_version_consistency.py",
]
missing = [p for p in required if not (ROOT / p).is_file()]
if missing:
    raise SystemExit("Missing required files: " + ", ".join(missing))

for forbidden in (
    ROOT / "paper",
    ROOT / "release-artifacts",
    ROOT / "REPOSITORY_RENAME.md",
    ROOT / "docs/maintainers/rename-repository.md",
):
    if forbidden.exists():
        raise SystemExit(f"Obsolete or standalone-paper path must be removed: {forbidden.relative_to(ROOT)}")

for path in ROOT.rglob("*"):
    if not path.is_file():
        continue
    rel = path.relative_to(ROOT)
    if rel.parts and rel.parts[0] in {"release", ".lake", "site", ".git", ".venv", ".venv-docs"}:
        continue
    if rel.parts[:2] == ("docs", "generated"):
        continue
    if path.suffix.lower() in {".pdf", ".zip"}:
        raise SystemExit(f"Tracked standalone binary is forbidden: {rel}")

manifest = json.loads((ROOT / "archive/theorem-manifest.json").read_text(encoding="utf-8"))
if manifest.get("schema_version") != 4:
    raise SystemExit("Theorem manifest schema mismatch")
if manifest.get("version") != version:
    raise SystemExit("Theorem manifest version mismatch")
if manifest.get("publication_model") != project["publication_model"]:
    raise SystemExit("Publication model mismatch")
if manifest["upstream"]["commit"] != upstream:
    raise SystemExit("Unexpected upstream commit in theorem manifest")

endpoints = manifest.get("endpoints", [])
expected_names = {
    "normalizedRootedChildFactorialTreeBound",
    "markedRootLeafGeometricBound",
    "targetPreservingWeightedTreeBound",
}
if {e.get("public_name") for e in endpoints} != expected_names:
    raise SystemExit("Unexpected publication endpoint set")

wrapper = (ROOT / "MarkedRootedClosure/PaperTheorems.lean").read_text(encoding="utf-8")
for name in expected_names:
    if not re.search(rf"\btheorem\s+{re.escape(name)}\b", wrapper):
        raise SystemExit(f"Public theorem missing from wrapper: {name}")

for rel in (
    "project.json",
    "lake-manifest.json",
    "archive/theorem-manifest.json",
    "archive/proof-dag.json",
    "archive/actions-manifest.json",
    "docs/paper/manifest.json",
    "codemeta.json",
    ".zenodo.json",
    "schemas/project.schema.json",
    "schemas/theorem-manifest.schema.json",
    "schemas/paper-manifest.schema.json",
    "schemas/buildinfo.schema.json",
    "schemas/release-index.schema.json",
    "schemas/actions-manifest.schema.json",
    "schemas/citation-cff.schema.json",
    "schemas/proof-dag.schema.json",
    "schemas/provenance.schema.json",
):
    json.loads((ROOT / rel).read_text(encoding="utf-8"))

for rel in (
    "CITATION.cff",
    "CITATION.bib",
    "codemeta.json",
    ".zenodo.json",
    "CHANGELOG.md",
    "RELEASE_NOTES.md",
):
    if version not in (ROOT / rel).read_text(encoding="utf-8"):
        raise SystemExit(f"Version {version} missing from {rel}")

all_text: list[tuple[Path, str]] = []
for path in ROOT.rglob("*"):
    if not path.is_file() or path.suffix.lower() in {".png", ".jpg", ".jpeg"}:
        continue
    rel = path.relative_to(ROOT)
    if rel in {Path("scripts/check_artifact.py"), Path("scripts/check_project_identity.py")}:
        continue
    if any(part in {".git", ".lake", "site", "release", ".venv", ".venv-docs", "__pycache__"}
           for part in rel.parts):
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    all_text.append((path, text))

for path, text in all_text:
    rel = path.relative_to(ROOT)
    for stale in (
        "paper/main.pdf",
        "paper/main.tex",
        "release-artifacts/",
        "Uploading this v2 tree",
    ):
        if stale in text:
            raise SystemExit(f"Stale standalone-publication reference {stale!r} in {rel}")

makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
lean_block = makefile.split("lean:", 1)[1].split("\n\n", 1)[0]
if "lake update" in lean_block:
    raise SystemExit("ordinary Lean verification must not refresh dependency locks")
if "lock-refresh:" not in makefile or "lake update" not in makefile.split("lock-refresh:", 1)[1]:
    raise SystemExit("explicit lock-refresh target is missing")
lock_refresh_block = makefile.split("lock-refresh:", 1)[1].split("\n\n", 1)[0]
if "scripts/process_runner.py" not in lock_refresh_block:
    raise SystemExit("lock-refresh must supervise lake update")
for command in (
    "scripts/check_version_consistency.py",
    "scripts/check_python_lock.py",
    "scripts/check_source_manifest.py",
    "scripts/check_proof_dag.py",
    "scripts/check_accessibility.py",
    "scripts/generate_provenance.py",
    "scripts/process_runner.py",
    "scripts/run_lean_gate.py",
):
    if command not in makefile:
        raise SystemExit(f"Makefile audit/evidence command missing: {command}")
for target in ("test:", "syntax:", "smoke-release:", "evidence:", "package-determinism:"):
    if target not in makefile:
        raise SystemExit(f"Makefile target missing: {target}")

requirements_text = (ROOT / "requirements-docs.txt").read_text(encoding="utf-8")
requirements_lock = (ROOT / "requirements-docs.lock").read_text(encoding="utf-8")
for forbidden_dependency in ("cffconvert", "mkdocs-minify-plugin", "csscompressor", "htmlmin2"):
    if forbidden_dependency in requirements_text.casefold() or forbidden_dependency in requirements_lock.casefold():
        raise SystemExit(f"Conflicting or unnecessary Python dependency is forbidden: {forbidden_dependency}")

full = ROOT / "docs/generated/full-article.md"
if full.exists() and not full.read_text(encoding="utf-8").startswith("<!-- GENERATED FILE:"):
    raise SystemExit("generated full article lacks its do-not-edit marker")

png = ROOT / "docs/assets/images/proof-pipeline.png"
if png.stat().st_size < 20_000 or not png.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"):
    raise SystemExit("Graphical abstract is missing or invalid")

print("artifact audit: OK")
print(f"version: {version}")
print(f"publication endpoints: {len(endpoints)}")
print(f"upstream commit: {upstream}")
print("paper model: canonical sections + generated continuous HTML view")
