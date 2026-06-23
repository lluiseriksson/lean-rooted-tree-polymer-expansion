#!/usr/bin/env python3
"""Run the dependency-free source-tree audit in one deterministic process."""
from __future__ import annotations

import os
import runpy
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKS = [
    "scripts/assemble_paper.py",
    "scripts/check_project_identity.py",
    "scripts/check_version_consistency.py",
    "scripts/check_python_lock.py",
    "scripts/check_lake_lock.py",
    "scripts/check_paper_manifest.py",
    "scripts/check_theorem_manifest.py",
    "scripts/check_proof_dag.py",
    "scripts/check_references.py",
    "scripts/check_agent_index.py",
    "scripts/check_workflows.py",
    "scripts/check_artifact.py",
    "scripts/check_internal_links.py",
    "scripts/check_accessibility.py",
    "scripts/check_metadata.py",
]


def main() -> None:
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    print("clean-room: dependency-free unit tests", flush=True)
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        raise SystemExit("clean-room unit tests failed")

    print("clean-room: Lean placeholder audit", flush=True)
    subprocess.run(
        ["bash", "scripts/check_no_placeholders.sh"],
        cwd=ROOT,
        check=True,
        timeout=60,
    )

    for relative in CHECKS:
        print(f"clean-room: {relative}", flush=True)
        runpy.run_path(str(ROOT / relative), run_name="__main__")
    print("dependency-free clean-room audit: OK", flush=True)


if __name__ == "__main__":
    main()
