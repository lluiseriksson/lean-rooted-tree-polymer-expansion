#!/usr/bin/env python3
"""Generate a deterministic CycloneDX 1.5 SBOM from committed lock files."""
from __future__ import annotations

import hashlib
import json
import uuid
from pathlib import Path
from urllib.parse import urlparse

from project_config import ROOT, load_project, release_stem, repository_url, site_url
from python_requirements import canonical_name, parse_exact_requirements, requirement_map


def purl_for_git(name: str, url: str, rev: str) -> str:
    parsed = urlparse(url)
    if parsed.netloc == "github.com":
        path = parsed.path.removesuffix(".git").strip("/")
        return f"pkg:github/{path}@{rev}"
    return f"pkg:generic/{name}@{rev}"


def locked_python_requirements(root: Path = ROOT) -> list[tuple[str, str]]:
    project = load_project(root)
    return parse_exact_requirements(root / project["python_lock"])


def main() -> None:
    project = load_project()
    release_dir = ROOT / "release"
    release_dir.mkdir(parents=True, exist_ok=True)
    out = release_dir / f"{release_stem(project)}.cdx.json"
    lake = json.loads((ROOT / "lake-manifest.json").read_text(encoding="utf-8"))
    direct = requirement_map(ROOT / "requirements-docs.txt")

    root_ref = f"pkg:github/{project['repository_owner']}/{project['repository_slug']}@{project['version']}"
    components: list[dict[str, object]] = []
    dependency_refs: list[str] = []

    elan_ref = f"pkg:github/leanprover/elan@{project['elan_installer_commit']}"
    dependency_refs.append(elan_ref)
    components.append({
        "type": "application",
        "scope": "optional",
        "bom-ref": elan_ref,
        "name": "leanprover/elan installer",
        "version": project["elan_installer_commit"],
        "purl": elan_ref,
        "externalReferences": [{
            "type": "vcs",
            "url": "https://github.com/leanprover/elan/blob/" + project["elan_installer_commit"] + "/elan-init.sh",
        }],
        "properties": [
            {"name": "dependency.role", "value": "container-bootstrap"},
            {"name": "git.blob", "value": project["elan_installer_blob_sha"]},
        ],
    })

    for pkg in lake.get("packages", []):
        ref = purl_for_git(pkg["name"], pkg["url"], pkg["rev"])
        dependency_refs.append(ref)
        components.append({
            "type": "library",
            "bom-ref": ref,
            "name": pkg["name"],
            "version": pkg["rev"],
            "purl": ref,
            "externalReferences": [{"type": "vcs", "url": pkg["url"]}],
            "properties": [
                {"name": "lean.manifest.inputRev", "value": str(pkg.get("inputRev", ""))},
                {"name": "lean.manifest.inherited", "value": str(pkg.get("inherited", False)).lower()},
            ],
        })

    actions_manifest = json.loads((ROOT / "archive/actions-manifest.json").read_text(encoding="utf-8"))
    action_labels = actions_manifest.get("labels", {})
    for action, version in sorted(actions_manifest["actions"].items()):
        ref = f"pkg:github/{action}@{version}"
        dependency_refs.append(ref)
        components.append({
            "type": "application",
            "scope": "optional",
            "bom-ref": ref,
            "name": action,
            "version": version,
            "purl": ref,
            "externalReferences": [{"type": "vcs", "url": f"https://github.com/{action}"}],
            "properties": [
                {"name": "dependency.role", "value": "github-actions-build"},
                {"name": "github.action.tag", "value": action_labels.get(action, "unknown")},
            ],
        })

    for name, version in locked_python_requirements():
        canonical = canonical_name(name)
        ref = f"pkg:pypi/{canonical}@{version}"
        dependency_refs.append(ref)
        components.append({
            "type": "library",
            "bom-ref": ref,
            "name": name,
            "version": version,
            "purl": ref,
            "externalReferences": [{
                "type": "distribution",
                "url": f"https://pypi.org/project/{name}/{version}/",
            }],
            "properties": [
                {"name": "dependency.role", "value": "documentation"},
                {"name": "dependency.scope", "value": "direct" if canonical in direct else "transitive"},
                {"name": "dependency.lock", "value": project["python_lock"]},
            ],
        })

    serial = uuid.uuid5(uuid.NAMESPACE_URL, f"{repository_url(project)}/releases/tag/v{project['version']}#cyclonedx")
    document = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.5",
        "serialNumber": f"urn:uuid:{serial}",
        "version": 1,
        "metadata": {
            "timestamp": f"{project['release_date']}T12:00:00Z",
            "tools": {"components": [{
                "type": "application",
                "name": "generate_cyclonedx.py",
                "version": project["version"],
            }]},
            "authors": [{"name": "Lluis Eriksson"}],
            "component": {
                "type": "application",
                "bom-ref": root_ref,
                "name": project["repository_slug"],
                "version": project["version"],
                "purl": root_ref,
                "licenses": [{"license": {"id": "AGPL-3.0-or-later"}}],
                "externalReferences": [
                    {"type": "vcs", "url": repository_url(project)},
                    {"type": "website", "url": site_url(project)},
                ],
            },
        },
        "components": components,
        "dependencies": [
            {"ref": root_ref, "dependsOn": sorted(dependency_refs)},
            *({"ref": ref, "dependsOn": []} for ref in sorted(dependency_refs)),
        ],
    }
    out.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    digest = hashlib.sha256(out.read_bytes()).hexdigest()
    out.with_suffix(out.suffix + ".sha256").write_text(f"{digest}  {out.name}\n", encoding="utf-8")
    print(f"CycloneDX SBOM created: {out}")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
