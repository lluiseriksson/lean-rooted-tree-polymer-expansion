#!/usr/bin/env python3
"""Generate a compact SPDX 2.3 JSON SBOM from committed dependency locks."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from project_config import ROOT, load_project, release_stem, repository_url

project = load_project()
release_dir = ROOT / "release"
release_dir.mkdir(parents=True, exist_ok=True)
out = release_dir / f"{release_stem(project)}.spdx.json"

lake = json.loads((ROOT / "lake-manifest.json").read_text(encoding="utf-8"))
requirements: list[tuple[str, str]] = []
for line in (ROOT / "requirements-docs.txt").read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    match = re.fullmatch(r"([A-Za-z0-9_.-]+)==([^\s]+)", line)
    if not match:
        raise SystemExit(f"unlocked documentation requirement: {line}")
    requirements.append((match.group(1), match.group(2)))

packages = [
    {
        "SPDXID": "SPDXRef-Package-Root",
        "name": project["repository_slug"],
        "versionInfo": project["version"],
        "downloadLocation": repository_url(project),
        "filesAnalyzed": False,
        "licenseConcluded": "AGPL-3.0-or-later",
        "licenseDeclared": "AGPL-3.0-or-later",
        "copyrightText": "Copyright 2026 Lluis Eriksson",
    }
]
relationships = []
for pkg in lake.get("packages", []):
    safe = re.sub(r"[^A-Za-z0-9.-]", "-", pkg["name"])
    spdx_id = f"SPDXRef-Lean-{safe}"
    packages.append(
        {
            "SPDXID": spdx_id,
            "name": pkg["name"],
            "versionInfo": pkg["rev"],
            "downloadLocation": pkg["url"],
            "filesAnalyzed": False,
            "licenseConcluded": "NOASSERTION",
            "licenseDeclared": "NOASSERTION",
            "copyrightText": "NOASSERTION",
            "externalRefs": [
                {
                    "referenceCategory": "PACKAGE-MANAGER",
                    "referenceType": "purl",
                    "referenceLocator": "pkg:generic/" + pkg["name"] + "@" + pkg["rev"],
                }
            ],
        }
    )
    relationships.append(
        {
            "spdxElementId": "SPDXRef-Package-Root",
            "relationshipType": "DEPENDS_ON",
            "relatedSpdxElement": spdx_id,
        }
    )
for name, version in requirements:
    safe = re.sub(r"[^A-Za-z0-9.-]", "-", name)
    spdx_id = f"SPDXRef-Python-{safe}"
    packages.append(
        {
            "SPDXID": spdx_id,
            "name": name,
            "versionInfo": version,
            "downloadLocation": f"https://pypi.org/project/{name}/{version}/",
            "filesAnalyzed": False,
            "licenseConcluded": "NOASSERTION",
            "licenseDeclared": "NOASSERTION",
            "copyrightText": "NOASSERTION",
            "externalRefs": [
                {
                    "referenceCategory": "PACKAGE-MANAGER",
                    "referenceType": "purl",
                    "referenceLocator": f"pkg:pypi/{name.lower()}@{version}",
                }
            ],
        }
    )
    relationships.append(
        {
            "spdxElementId": "SPDXRef-Package-Root",
            "relationshipType": "DEPENDS_ON",
            "relatedSpdxElement": spdx_id,
        }
    )

document = {
    "spdxVersion": "SPDX-2.3",
    "dataLicense": "CC0-1.0",
    "SPDXID": "SPDXRef-DOCUMENT",
    "name": f"{release_stem(project)}-source-sbom",
    "documentNamespace": (
        f"{repository_url(project)}/releases/tag/v{project['version']}#sbom"
    ),
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
digest = hashlib.sha256(out.read_bytes()).hexdigest()
sidecar = out.with_suffix(out.suffix + ".sha256")
sidecar.write_text(f"{digest}  {out.name}\n", encoding="utf-8")
print(f"SBOM created: {out}")
print(f"sha256: {digest}")
