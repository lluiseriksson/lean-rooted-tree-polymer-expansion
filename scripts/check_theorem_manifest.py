#!/usr/bin/env python3
"""Cross-check the machine-readable theorem manifest against code and prose."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from project_config import ROOT, load_project, repository_url, site_url
from lean_signatures import signature_sha256

EXPECTED_PUBLIC_NAMES = {
    "normalizedRootedChildFactorialTreeBound",
    "markedRootLeafGeometricBound",
    "targetPreservingWeightedTreeBound",
}
EXPECTED_FALSE_CLAIMS = {
    "proves_model_specific_raw_yang_mills_activity",
    "proves_hRpoly",
    "proves_continuum_limit",
    "proves_mass_gap",
}


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    project = load_project(root)
    manifest = _load(root / "archive" / "theorem-manifest.json")

    if manifest.get("schema_version") != 4:
        errors.append("theorem manifest schema_version must be 4")
    if manifest.get("artifact") != project["artifact_title"]:
        errors.append("theorem manifest artifact title differs from project.json")
    if manifest.get("version") != project["version"]:
        errors.append("theorem manifest version differs from project.json")
    if manifest.get("publication_model") != project["publication_model"]:
        errors.append("theorem manifest publication model differs from project.json")
    if manifest.get("proof_dag") != project["proof_dag"]:
        errors.append("theorem manifest proof_dag differs from project.json")

    upstream = manifest.get("upstream", {})
    expected_upstream = {
        "repository": project["upstream_repository"],
        "commit": project["upstream_commit"],
        "lean": project["lean_toolchain"],
        "mathlib": project["mathlib_commit"],
    }
    for key, expected in expected_upstream.items():
        if upstream.get(key) != expected:
            errors.append(f"theorem manifest upstream.{key} mismatch")

    repository = manifest.get("repository", {})
    expected_repo = {
        "url": repository_url(project),
        "site": site_url(project),
        "slug": project["repository_slug"],
    }
    for key, expected in expected_repo.items():
        if repository.get(key) != expected:
            errors.append(f"theorem manifest repository.{key} mismatch")

    endpoints = manifest.get("endpoints")
    if not isinstance(endpoints, list):
        errors.append("theorem manifest endpoints must be a list")
        endpoints = []
    names = [e.get("public_name") for e in endpoints if isinstance(e, dict)]
    if set(names) != EXPECTED_PUBLIC_NAMES:
        errors.append(f"unexpected public endpoint set: {sorted(n for n in names if n)}")
    if len(names) != len(set(names)):
        errors.append("duplicate public theorem name in theorem manifest")

    wrapper_path = root / "MarkedRootedClosure" / "PaperTheorems.lean"
    wrapper = wrapper_path.read_text(encoding="utf-8")
    wrapper_meta = manifest.get("wrapper", {})
    if wrapper_meta.get("path") != "MarkedRootedClosure/PaperTheorems.lean":
        errors.append("theorem manifest wrapper path mismatch")
    import hashlib
    wrapper_digest = hashlib.sha256(wrapper_path.read_bytes()).hexdigest()
    if wrapper_meta.get("sha256") != wrapper_digest:
        errors.append("theorem manifest wrapper sha256 mismatch")
    if manifest.get("oracle_axioms") != ["propext", "Classical.choice", "Quot.sound"]:
        errors.append("theorem manifest oracle_axioms mismatch")
    lock_text = (root / "archive" / "UPSTREAM.lock").read_text(encoding="utf-8")
    lock_values = {}
    for line in lock_text.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            lock_values[key] = value
    expected_source_blobs = {
        "YangMills/KP/RootedLeafSummation.lean": lock_values.get("ROOTED_LEAF_BLOB_SHA"),
        "YangMills/RG/AppendixFSecondUrsellLeafSummation.lean": lock_values.get("APPENDIX_F_LEAF_BLOB_SHA"),
    }
    formal_map = (root / "docs" / "formalization" / "index.md").read_text(encoding="utf-8")
    artifact_map = (root / "docs" / "artifact" / "theorem-map.md").read_text(encoding="utf-8")

    qualified_seen: set[str] = set()
    upstream_seen: set[str] = set()
    for endpoint in endpoints:
        if not isinstance(endpoint, dict):
            errors.append("non-object endpoint in theorem manifest")
            continue
        public = endpoint.get("public_name", "")
        qualified = endpoint.get("qualified_public_name", "")
        upstream_name = endpoint.get("upstream_name", "")
        source = endpoint.get("source", "")
        paper_page = endpoint.get("paper_page", "")
        source_blob_sha = endpoint.get("source_blob_sha", "")
        public_signature_sha256 = endpoint.get("public_signature_sha256", "")
        source_excerpt = endpoint.get("source_excerpt", "")
        source_excerpt_sha256 = endpoint.get("source_excerpt_sha256", "")

        if qualified != f"MarkedRootedClosure.{public}":
            errors.append(f"qualified name mismatch for {public}")
        if qualified in qualified_seen:
            errors.append(f"duplicate qualified theorem name: {qualified}")
        qualified_seen.add(qualified)
        if upstream_name in upstream_seen:
            errors.append(f"duplicate upstream theorem name: {upstream_name}")
        upstream_seen.add(upstream_name)

        if not re.search(rf"\btheorem\s+{re.escape(public)}\b", wrapper):
            errors.append(f"wrapper theorem missing: {public}")
        upstream_short = upstream_name.rsplit(".", 1)[-1]
        if upstream_short not in wrapper:
            errors.append(f"wrapper does not reference upstream theorem: {upstream_name}")
        if not source.startswith("YangMills/") or not source.endswith(".lean"):
            errors.append(f"invalid upstream source path for {public}: {source}")
        if not re.fullmatch(r"[0-9a-f]{40}", source_blob_sha):
            errors.append(f"invalid source blob SHA for {public}")
        elif expected_source_blobs.get(source) != source_blob_sha:
            errors.append(f"source blob SHA differs from UPSTREAM.lock for {public}")
        try:
            actual_signature = signature_sha256(wrapper, public)
        except (KeyError, ValueError) as exc:
            errors.append(f"cannot fingerprint wrapper theorem {public}: {exc}")
        else:
            if public_signature_sha256 != actual_signature:
                errors.append(f"public signature hash mismatch for {public}")
        excerpt_path = root / source_excerpt
        if not excerpt_path.is_file():
            errors.append(f"source excerpt missing for {public}: {source_excerpt}")
        else:
            actual_excerpt = hashlib.sha256(excerpt_path.read_bytes()).hexdigest()
            if source_excerpt_sha256 != actual_excerpt:
                errors.append(f"source excerpt hash mismatch for {public}")
            if upstream_short not in excerpt_path.read_text(encoding="utf-8"):
                errors.append(f"source excerpt does not contain upstream theorem {upstream_name}")

        page = root / paper_page
        if not page.is_file():
            errors.append(f"paper page missing for {public}: {paper_page}")
        elif qualified not in page.read_text(encoding="utf-8"):
            errors.append(f"paper page does not name public endpoint {qualified}")

        for label, text in (("formalization map", formal_map), ("artifact theorem map", artifact_map)):
            if qualified not in text:
                errors.append(f"{label} does not contain {qualified}")
            if upstream_name not in text:
                errors.append(f"{label} does not contain {upstream_name}")

    boundary = manifest.get("claim_boundary", {})
    for key in EXPECTED_FALSE_CLAIMS:
        if boundary.get(key) is not False:
            errors.append(f"claim boundary {key} must be false")

    lock = (root / "archive" / "UPSTREAM.lock").read_text(encoding="utf-8")
    for needle in (project["upstream_commit"], project["lean_toolchain"], project["mathlib_commit"]):
        if needle not in lock:
            errors.append(f"UPSTREAM.lock missing {needle}")
    return errors


def main() -> None:
    errors = validate(ROOT)
    if errors:
        raise SystemExit("Theorem manifest audit failed:\n" + "\n".join(f"- {e}" for e in errors))
    print(f"theorem manifest audit: OK ({len(EXPECTED_PUBLIC_NAMES)} public endpoints)")


if __name__ == "__main__":
    main()
