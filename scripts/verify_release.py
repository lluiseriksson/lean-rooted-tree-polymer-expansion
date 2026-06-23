#!/usr/bin/env python3
"""Verify source archive safety, manifests, SBOMs, provenance, and build evidence."""
from __future__ import annotations

import hashlib
import json
import stat
import sys
import unicodedata
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any

from archive_safety import MAX_MEMBER_BYTES, MAX_TOTAL_BYTES, validated_members
from project_config import ROOT, load_project, release_stem
from python_requirements import canonical_name, parse_exact_requirements, requirement_map


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _sidecar_ok(path: Path) -> None:
    sidecar = path.with_suffix(path.suffix + ".sha256")
    if not sidecar.is_file():
        raise ValueError(f"missing checksum sidecar: {sidecar}")
    parts = sidecar.read_text(encoding="utf-8").strip().split()
    if len(parts) < 2 or parts[1] != path.name:
        raise ValueError(f"malformed checksum sidecar: {sidecar}")
    if parts[0] != sha256(path):
        raise ValueError(f"checksum mismatch for {path.name}")


def _schema_validate(path: Path, schema_path: Path) -> None:
    try:
        import jsonschema  # type: ignore
    except ImportError:
        return
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    data = json.loads(path.read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator(schema).validate(data)


def verify_zip(zip_path: Path, project: dict[str, Any]) -> str:
    stem = release_stem(project)
    if not zip_path.is_file():
        raise ValueError(f"no release ZIP found: {zip_path}")
    _sidecar_ok(zip_path)
    actual = sha256(zip_path)

    with zipfile.ZipFile(zip_path) as archive:
        bad = archive.testzip()
        if bad:
            raise ValueError(f"corrupt ZIP member: {bad}")
        infos = validated_members(archive)
        if not infos:
            raise ValueError("release ZIP is empty")
        raw_names = [info.filename for info in infos]
        normalised = [unicodedata.normalize("NFC", name) for name in raw_names]
        names = [PurePosixPath(name) for name in normalised]
        roots = {name.parts[0] for name in names if name.parts}
        if roots != {stem}:
            raise ValueError(f"archive root mismatch: expected {stem}, found {roots}")
        if sum(info.file_size for info in infos) > MAX_TOTAL_BYTES:
            raise ValueError("source archive exceeds uncompressed safety limit")
        if any(info.file_size > MAX_MEMBER_BYTES for info in infos):
            raise ValueError("source archive contains an oversized member")

        rel_names: set[PurePosixPath] = set()
        for info, name in zip(infos, names):
            if name.is_absolute() or ".." in name.parts:
                raise ValueError(f"unsafe archive path: {name}")
            mode = (info.external_attr >> 16) & 0xFFFF
            file_type = stat.S_IFMT(mode)
            if file_type == stat.S_IFLNK:
                raise ValueError(f"symlink forbidden in source archive: {name}")
            if file_type not in (0, stat.S_IFREG):
                raise ValueError(f"non-regular ZIP member forbidden: {name}")
            if info.flag_bits & 0x1:
                raise ValueError(f"encrypted ZIP member forbidden: {name}")
            rel_names.add(PurePosixPath(*name.parts[1:]))

        manifest_name = PurePosixPath("MANIFEST.sha256")
        if manifest_name not in rel_names:
            raise ValueError("archive-local MANIFEST.sha256 is missing")

        forbidden_top = {
            "paper", "release-artifacts", ".git", ".lake", "site", "release",
            "docs/generated",
        }
        forbidden_anywhere = {".git", ".lake", "__pycache__", ".pytest_cache"}
        for rel in rel_names:
            text = rel.as_posix()
            if any(text == item or text.startswith(item + "/") for item in forbidden_top):
                raise ValueError(f"forbidden path in archive: {rel}")
            if any(part in forbidden_anywhere for part in rel.parts):
                raise ValueError(f"forbidden path in archive: {rel}")
            if rel.suffix.lower() in {".pdf", ".zip"}:
                raise ValueError(f"forbidden tracked binary in source archive: {rel}")

        required = {
            PurePosixPath("README.md"),
            PurePosixPath("project.json"),
            PurePosixPath("REPOSITORY_HISTORY.md"),
            PurePosixPath("lake-manifest.json"),
            PurePosixPath("requirements-docs.txt"),
            PurePosixPath("requirements-docs.lock"),
            PurePosixPath("MarkedRootedClosure/PaperTheorems.lean"),
            PurePosixPath("docs/paper/index.md"),
            PurePosixPath("docs/paper/manifest.json"),
            PurePosixPath("docs/formalization/index.md"),
            PurePosixPath("docs/artifact/theorem-map.md"),
            PurePosixPath("docs/artifact/proof-dependency-graph.md"),
            PurePosixPath("docs/artifact/verification-contract.md"),
            PurePosixPath("docs/artifact/release-evidence.md"),
            PurePosixPath("archive/UPSTREAM.lock"),
            PurePosixPath("archive/theorem-manifest.json"),
            PurePosixPath("archive/proof-dag.json"),
            PurePosixPath("archive/actions-manifest.json"),
            PurePosixPath("schemas/project.schema.json"),
            PurePosixPath("schemas/theorem-manifest.schema.json"),
            PurePosixPath("schemas/proof-dag.schema.json"),
            PurePosixPath("schemas/citation-cff.schema.json"),
            PurePosixPath("schemas/provenance.schema.json"),
            PurePosixPath("schemas/buildinfo.schema.json"),
            PurePosixPath("schemas/release-index.schema.json"),
            PurePosixPath("scripts/check_version_consistency.py"),
            PurePosixPath("scripts/check_python_lock.py"),
            PurePosixPath("scripts/check_proof_dag.py"),
            PurePosixPath("scripts/check_accessibility.py"),
            PurePosixPath("scripts/archive_safety.py"),
            PurePosixPath("scripts/generate_provenance.py"),
            PurePosixPath("scripts/verify_release.py"),
            PurePosixPath("tests/test_archive_safety.py"),
            PurePosixPath("tests/test_metadata_schema.py"),
            PurePosixPath("tests/test_proof_dag.py"),
            PurePosixPath("tests/test_provenance.py"),
            PurePosixPath("tests/test_python_lock.py"),
            PurePosixPath("tests/test_version_consistency.py"),
            PurePosixPath("mkdocs.yml"),
        }
        missing = required - rel_names
        if missing:
            raise ValueError("missing required archive members: " + ", ".join(map(str, sorted(missing))))

        manifest_text = archive.read(f"{stem}/MANIFEST.sha256").decode("utf-8")
        listed: dict[PurePosixPath, str] = {}
        for line in manifest_text.splitlines():
            if not line.strip():
                continue
            try:
                digest, rel_text = line.split("  ", 1)
            except ValueError as exc:
                raise ValueError(f"malformed manifest row: {line!r}") from exc
            if len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest):
                raise ValueError(f"invalid manifest digest: {digest!r}")
            rel = PurePosixPath(rel_text)
            if rel in listed:
                raise ValueError(f"duplicate manifest entry: {rel}")
            listed[rel] = digest
            member = f"{stem}/{rel.as_posix()}"
            try:
                data = archive.read(member)
            except KeyError as exc:
                raise ValueError(f"manifest member missing from ZIP: {rel}") from exc
            if hashlib.sha256(data).hexdigest() != digest:
                raise ValueError(f"manifest digest mismatch for {rel}")
        unlisted = rel_names - set(listed) - {manifest_name}
        if unlisted:
            raise ValueError("unlisted ZIP members: " + ", ".join(map(str, sorted(unlisted))))

        archived_project = json.loads(archive.read(f"{stem}/project.json"))
        for key in ("version", "repository_slug", "upstream_commit", "mathlib_commit"):
            if archived_project.get(key) != project.get(key):
                raise ValueError(f"archived project mismatch: {key}")
        archived_lake = json.loads(archive.read(f"{stem}/lake-manifest.json"))
        revisions = {pkg["name"]: pkg["rev"] for pkg in archived_lake["packages"]}
        if revisions.get("YangMills") != project["upstream_commit"]:
            raise ValueError("archived upstream dependency mismatch")
        if revisions.get("mathlib") != project["mathlib_commit"]:
            raise ValueError("archived Mathlib dependency mismatch")
    return actual


def _verify_sboms(spdx_path: Path, cdx_path: Path, project: dict[str, Any]) -> None:
    spdx = _load_json(spdx_path)
    if spdx.get("spdxVersion") != "SPDX-2.3":
        raise ValueError("SPDX document version mismatch")
    if "SPDXRef-Package-Root" not in spdx.get("documentDescribes", []):
        raise ValueError("SPDX document does not describe the root package")
    spdx_packages = {item.get("name"): item for item in spdx.get("packages", []) if isinstance(item, dict)}
    if "leanprover/elan installer" not in spdx_packages:
        raise ValueError("SPDX document omits the pinned elan installer")

    cdx = _load_json(cdx_path)
    if cdx.get("bomFormat") != "CycloneDX" or cdx.get("specVersion") != "1.5":
        raise ValueError("CycloneDX document version mismatch")
    if cdx.get("metadata", {}).get("component", {}).get("version") != project["version"]:
        raise ValueError("CycloneDX root component version mismatch")
    cdx_components = {item.get("name"): item for item in cdx.get("components", []) if isinstance(item, dict)}
    if "leanprover/elan installer" not in cdx_components:
        raise ValueError("CycloneDX document omits the pinned elan installer")

    action_manifest = json.loads((ROOT / "archive/actions-manifest.json").read_text(encoding="utf-8"))
    for action, ref in action_manifest.get("actions", {}).items():
        if spdx_packages.get(action, {}).get("versionInfo") != ref:
            raise ValueError(f"SPDX action pin mismatch: {action}")
        if cdx_components.get(action, {}).get("version") != ref:
            raise ValueError(f"CycloneDX action pin mismatch: {action}")

    direct = requirement_map(ROOT / "requirements-docs.txt")
    locked = parse_exact_requirements(ROOT / project["python_lock"])
    for name, version in locked:
        if spdx_packages.get(name, {}).get("versionInfo") != version:
            raise ValueError(f"SPDX Python lock mismatch: {name}")
        component = cdx_components.get(name, {})
        if component.get("version") != version:
            raise ValueError(f"CycloneDX Python lock mismatch: {name}")
        props = {p.get("name"): p.get("value") for p in component.get("properties", []) if isinstance(p, dict)}
        expected_scope = "direct" if canonical_name(name) in direct else "transitive"
        if props.get("dependency.scope") != expected_scope:
            raise ValueError(f"CycloneDX Python scope mismatch: {name}")


def _verify_provenance(path: Path, artifacts: dict[str, Path], project: dict[str, Any]) -> None:
    lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(lines) != 1:
        raise ValueError("provenance JSONL must contain exactly one statement")
    statement = json.loads(lines[0])
    if statement.get("_type") != "https://in-toto.io/Statement/v1":
        raise ValueError("in-toto statement type mismatch")
    if statement.get("predicateType") != "https://slsa.dev/provenance/v1":
        raise ValueError("SLSA predicate type mismatch")
    subjects = {item.get("name"): item.get("digest", {}).get("sha256") for item in statement.get("subject", [])}
    for name in ("zip", "spdx", "cyclonedx", "buildinfo"):
        artifact = artifacts[name]
        if subjects.get(artifact.name) != sha256(artifact):
            raise ValueError(f"provenance subject mismatch: {artifact.name}")
    resolved = statement.get("predicate", {}).get("buildDefinition", {}).get("resolvedDependencies", [])
    deps = {(item.get("uri"), tuple(sorted(item.get("digest", {}).items()))) for item in resolved if isinstance(item, dict)}
    required = {
        (project["upstream_repository"] + ".git", (("gitCommit", project["upstream_commit"]),)),
        ("https://github.com/leanprover-community/mathlib4.git", (("gitCommit", project["mathlib_commit"]),)),
        ("file:" + project["python_lock"], (("sha256", sha256(ROOT / project["python_lock"])),)),
        ("file:archive/actions-manifest.json", (("sha256", sha256(ROOT / "archive/actions-manifest.json")),)),
    }
    if not required.issubset(deps):
        raise ValueError("provenance resolved dependency set is incomplete")


def verify_companion_files(zip_path: Path, project: dict[str, Any]) -> None:
    stem = release_stem(project)
    release_dir = zip_path.parent
    artifacts = {
        "zip": zip_path,
        "spdx": release_dir / f"{stem}.spdx.json",
        "cyclonedx": release_dir / f"{stem}.cdx.json",
        "buildinfo": release_dir / f"{stem}.buildinfo.json",
        "provenance": release_dir / f"{stem}.intoto.jsonl",
        "release_index": release_dir / f"{stem}.release.json",
    }
    for path in artifacts.values():
        if not path.is_file():
            raise ValueError(f"missing release companion: {path}")
        _sidecar_ok(path)

    _verify_sboms(artifacts["spdx"], artifacts["cyclonedx"], project)

    buildinfo = _load_json(artifacts["buildinfo"])
    if buildinfo.get("schema_version") != 2:
        raise ValueError("build-info schema mismatch")
    if buildinfo.get("project", {}).get("version") != project["version"]:
        raise ValueError("build-info project version mismatch")
    expected_sources = {
        "python_lock": project["python_lock"],
        "theorem_manifest": "archive/theorem-manifest.json",
        "proof_dag": project["proof_dag"],
        "paper_manifest": "docs/paper/manifest.json",
        "actions_manifest": "archive/actions-manifest.json",
        "source_manifest": "MANIFEST.sha256",
        "citation_schema": project["citation_schema"],
    }
    for key, rel in expected_sources.items():
        record = buildinfo.get("source_inputs", {}).get(key, {})
        if record.get("path") != rel or record.get("sha256") != sha256(ROOT / rel):
            raise ValueError(f"build-info source input mismatch: {key}")
    records = {item.get("name"): item for item in buildinfo.get("artifacts", []) if isinstance(item, dict)}
    for key in ("zip", "spdx", "cyclonedx"):
        path = artifacts[key]
        record = records.get(path.name)
        if not record or record.get("sha256") != sha256(path) or record.get("bytes") != path.stat().st_size:
            raise ValueError(f"build-info digest/size mismatch: {path.name}")

    _verify_provenance(artifacts["provenance"], artifacts, project)

    release_index = _load_json(artifacts["release_index"])
    if release_index.get("schema_version") != 2:
        raise ValueError("release-index schema mismatch")
    if release_index.get("release", {}).get("version") != project["version"]:
        raise ValueError("release-index version mismatch")
    index_records = {item.get("name"): item for item in release_index.get("artifacts", []) if isinstance(item, dict)}
    source_evidence = release_index.get("source_evidence", {})
    required_evidence = {
        "project_metadata": "project.json",
        "theorem_manifest": "archive/theorem-manifest.json",
        "proof_dag": project["proof_dag"],
        "paper_manifest": "docs/paper/manifest.json",
        "actions_manifest": "archive/actions-manifest.json",
        "python_lock": project["python_lock"],
        "citation_schema": project["citation_schema"],
        "source_manifest": "MANIFEST.sha256",
    }
    with zipfile.ZipFile(zip_path) as archive:
        for key, expected_path in required_evidence.items():
            record = source_evidence.get(key)
            if not isinstance(record, dict) or record.get("path") != expected_path:
                raise ValueError(f"release index source-evidence path mismatch: {key}")
            archived = archive.read(f"{stem}/{expected_path}")
            if record.get("sha256") != hashlib.sha256(archived).hexdigest():
                raise ValueError(f"release index source-evidence digest mismatch: {key}")
    for key in ("zip", "spdx", "cyclonedx", "buildinfo", "provenance"):
        path = artifacts[key]
        record = index_records.get(path.name)
        if not record or record.get("sha256") != sha256(path) or record.get("bytes") != path.stat().st_size:
            raise ValueError(f"release-index digest/size mismatch: {path.name}")

    checksums = release_dir / f"{stem}.checksums.sha256"
    if not checksums.is_file():
        raise ValueError(f"missing aggregate checksum file: {checksums}")
    checksum_rows: dict[str, str] = {}
    for line in checksums.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, name = line.split("  ", 1)
        if name in checksum_rows:
            raise ValueError(f"duplicate aggregate checksum entry: {name}")
        checksum_rows[name] = digest
    for path in artifacts.values():
        if checksum_rows.get(path.name) != sha256(path):
            raise ValueError(f"aggregate checksum mismatch: {path.name}")

    _schema_validate(artifacts["buildinfo"], ROOT / "schemas/buildinfo.schema.json")
    _schema_validate(artifacts["release_index"], ROOT / "schemas/release-index.schema.json")
    _schema_validate(artifacts["provenance"], ROOT / "schemas/provenance.schema.json")


def main() -> None:
    project = load_project()
    zip_path = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / "release" / f"{release_stem(project)}.zip"
    try:
        digest = verify_zip(zip_path, project)
        verify_companion_files(zip_path, project)
    except (ValueError, KeyError, json.JSONDecodeError, zipfile.BadZipFile) as exc:
        raise SystemExit(f"release verification failed: {exc}") from exc
    print(f"release verification: OK ({zip_path.name})")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
