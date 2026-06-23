#!/usr/bin/env python3
"""Ensure the machine-readable project index cannot drift from project metadata."""
from __future__ import annotations

from project_config import ROOT, load_project, repository_url, site_url

PUBLIC = (
    'MarkedRootedClosure.normalizedRootedChildFactorialTreeBound',
    'MarkedRootedClosure.markedRootLeafGeometricBound',
    'MarkedRootedClosure.targetPreservingWeightedTreeBound',
)


def validate() -> list[str]:
    project = load_project()
    path = ROOT / 'docs' / 'llms.txt'
    text = path.read_text(encoding='utf-8')
    needles = [
        repository_url(project),
        site_url(project),
        f"Version: {project['version']}",
        project['upstream_commit'],
        project['lean_toolchain'],
        project['mathlib_commit'],
        *PUBLIC,
        'does not prove the model-specific raw Yang--Mills activity estimate',
        'make verify-nonlean',
        'scripts/run_lean_gate.py',
        'scripts/release_inventory.py',
        'read-only verification transfers an exact candidate',
    ]
    return [f'llms.txt missing {needle!r}' for needle in needles if needle not in text]


def main() -> None:
    errors = validate()
    if errors:
        raise SystemExit('agent index audit failed:\n' + '\n'.join(f'- {e}' for e in errors))
    print('agent index audit: OK')


if __name__ == '__main__':
    main()
