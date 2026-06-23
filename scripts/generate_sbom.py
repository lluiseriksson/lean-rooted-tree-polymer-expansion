#!/usr/bin/env python3
"""Generate a deterministic SPDX 2.3 JSON SBOM from committed dependency locks."""
from __future__ import annotations

import json
import re
from pathlib import Path

from project_config import ROOT, load_project, release_stem, repository_url
from release_inventory import sha256, write_sidecar
from python_requirements import canonical_name, parse_exact_requirements, requirement_map



def main() -> None:
    project = load_project()
    release_dir = ROOT / "release"
    release_dir.mkdir(parents=True, exist_ok=True)
    out = release_dir / f"{release_stem(project)}.spdx.json"
    lake = json.loads((ROOT / "lake-manifest.json").read_text(encoding="utf-8"))
    direct = requirement_map(ROOT / "requirements-docs.txt")
    locked = parse_exact_requirements(ROOT / project["python_lock"])

    packages: list[dict[str, object]] = [{
        "SPDXID": "SPDXRef-Package-Root",
        "name": project["repository_slug"],
        "versionInfo": project["version"],
        "downloadLocation": repository_url(project),
        "filesAnalyzed": False,
        "licenseConcluded": "AGPL-3.0-or-later",
        "licenseDeclared": "AGPL-3.0-or-later",
        "copyrightText": "Copyright 2026 Lluis Eriksson",
        "comment": "Original documentation and figures are separately licensed CC-BY-4.0.",
    }]
    relationships: list[dict[str, str]] = []

    elan_ref = f"pkg:github/leanprover/elan@{project['elan_installer_commit']}"
    packages.append({
        "SPDXID": "SPDXRef-Elan-Installer",
        "name": "leanprover/elan installer",
        "versionInfo": project["elan_installer_commit"],
        "downloadLocation": (
            "https://github.com/leanprover/elan/blob/"
            + project["elan_installer_commit"] + "/elan-init.sh"
        ),
        "filesAnalyzed": False,
        "licenseConcluded": "NOASSERTION",
        "licenseDeclared": "NOASSERTION",
        "copyrightText": "NOASSERTION",
        "externalRefs": [{
            "referenceCategory": "PACKAGE-MANAGER",
            "referenceType": "purl",
            "referenceLocator": elan_ref,
        }],
        "comment": "Installer Git blob " + project["elan_installer_blob_sha"],
    })
    relationships.append({
        "spdxElementId": "SPDXRef-Elan-Installer",
        "relationshipType": "BUILD_DEPENDENCY_OF",
        "relatedSpdxElement": "SPDXRef-Package-Root",
    })

    for pkg in lake.get("packages", []):
        safe = re.sub(r"[^A-Za-z0-9.-]", "-", pkg["name"])
        spdx_id = f"SPDXRef-Lean-{safe}"
        packages.append({
            "SPDXID": spdx_id,
            "name": pkg["name"],
            "versionInfo": pkg["rev"],
            "downloadLocation": pkg["url"],
            "filesAnalyzed": False,
            "licenseConcluded": "NOASSERTION",
            "licenseDeclared": "NOASSERTION",
            "copyrightText": "NOASSERTION",
            "externalRefs": [{
                "referenceCategory": "PACKAGE-MANAGER",
                "referenceType": "purl",
                "referenceLocator": f"pkg:generic/{pkg['name']}@{pkg['rev']}",
            }],
        })
        relationships.append({
            "spdxElementId": "SPDXRef-Package-Root",
            "relationshipType": "DEPENDS_ON",
            "relatedSpdxElement": spdx_id,
        })

    actions_manifest = json.loads((ROOT / "archive/actions-manifest.json").read_text(encoding="utf-8"))
    action_labels = actions_manifest.get("labels", {})
    for action, ref in sorted(actions_manifest["actions"].items()):
        safe = re.sub(r"[^A-Za-z0-9.-]", "-", action)
        spdx_id = f"SPDXRef-Action-{safe}"
        packages.append({
            "SPDXID": spdx_id,
            "name": action,
            "versionInfo": ref,
            "downloadLocation": f"https://github.com/{action}",
            "filesAnalyzed": False,
            "licenseConcluded": "NOASSERTION",
            "licenseDeclared": "NOASSERTION",
            "copyrightText": "NOASSERTION",
            "externalRefs": [{
                "referenceCategory": "PACKAGE-MANAGER",
                "referenceType": "purl",
                "referenceLocator": f"pkg:github/{action}@{ref}",
            }],
            "comment": f"Resolved from audited action label {action_labels.get(action, 'unknown')}",
        })
        relationships.append({
            "spdxElementId": spdx_id,
            "relationshipType": "BUILD_DEPENDENCY_OF",
            "relatedSpdxElement": "SPDXRef-Package-Root",
        })

    for name, version in locked:
        canonical = canonical_name(name)
        safe = re.sub(r"[^A-Za-z0-9.-]", "-", canonical)
        spdx_id = f"SPDXRef-Python-{safe}"
        scope = "direct" if canonical in direct else "transitive"
        packages.append({
            "SPDXID": spdx_id,
            "name": name,
            "versionInfo": version,
            "downloadLocation": f"https://pypi.org/project/{name}/{version}/",
            "filesAnalyzed": False,
            "licenseConcluded": "NOASSERTION",
            "licenseDeclared": "NOASSERTION",
            "copyrightText": "NOASSERTION",
            "externalRefs": [{
                "referenceCategory": "PACKAGE-MANAGER",
                "referenceType": "purl",
                "referenceLocator": f"pkg:pypi/{canonical}@{version}",
            }],
            "comment": f"Python documentation dependency scope: {scope}; resolved by requirements-docs.lock",
        })
        relationships.append({
            "spdxElementId": "SPDXRef-Package-Root",
            "relationshipType": "DEPENDS_ON",
            "relatedSpdxElement": spdx_id,
        })

    document = {
        "spdxVersion": "SPDX-2.3",
        "dataLicense": "CC0-1.0",
        "SPDXID": "SPDXRef-DOCUMENT",
        "name": f"{release_stem(project)}-source-sbom",
        "documentNamespace": f"{repository_url(project)}/releases/tag/v{project['version']}#sbom",
        "creationInfo": {
            "created": f"{project['release_date']}T12:00:00Z",
            "creators": ["Tool: scripts/generate_sbom.py", "Person: Lluis Eriksson"],
            "licenseListVersion": "3.25",
        },
        "documentDescribes": ["SPDXRef-Package-Root"],
        "packages": packages,
        "relationships": relationships,
    }
    out.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    digest = sha256(out)
    write_sidecar(out)
    print(f"SBOM created: {out}")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
