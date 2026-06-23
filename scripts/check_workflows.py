#!/usr/bin/env python3
"""Audit GitHub Actions for minimum-permission and reproducibility invariants."""
from __future__ import annotations

import json
import re
from pathlib import Path

from project_config import ROOT, repository_full_name, load_project

WORKFLOWS = ROOT / '.github' / 'workflows'
REQUIRED = {'ci.yml', 'pages.yml', 'release.yml', 'dependency-review.yml', 'maintenance.yml'}
FORBIDDEN_REFS = ('@main', '@master', '@latest')
SHA_RE = re.compile(r'^[0-9a-f]{40}$')
USES_RE = re.compile(r'uses:\s*([^\s#]+)')


def validate(root: Path = ROOT) -> list[str]:
    workflows = root / '.github' / 'workflows'
    errors: list[str] = []
    missing = sorted(name for name in REQUIRED if not (workflows / name).is_file())
    if missing:
        errors.append('missing workflows: ' + ', '.join(missing))
        return errors

    manifest_path = root / 'archive' / 'actions-manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    expected_actions = manifest.get('actions', {})
    labels = manifest.get('labels', {})
    if (manifest.get('schema_version') != 2
            or manifest.get('policy') != 'immutable-commit-shas'
            or not isinstance(expected_actions, dict)
            or not isinstance(labels, dict)):
        errors.append('invalid actions-manifest.json')
        expected_actions = {}
        labels = {}
    elif set(labels) != set(expected_actions):
        errors.append('actions-manifest labels must have exactly the action keys')
    for action, ref in expected_actions.items():
        if not isinstance(ref, str) or not SHA_RE.fullmatch(ref):
            errors.append(f'actions manifest ref is not an immutable SHA: {action}={ref!r}')

    used_actions: dict[str, set[str]] = {}
    paths = sorted([*workflows.glob('*.yml'), *workflows.glob('*.yaml')])
    for path in paths:
        text = path.read_text(encoding='utf-8')
        rel = path.relative_to(root)
        if 'pull_request_target:' in text:
            errors.append(f'{rel}: pull_request_target is forbidden')
        if 'permissions:' not in text:
            errors.append(f'{rel}: explicit permissions block missing')
        if 'continue-on-error: true' in text:
            errors.append(f'{rel}: verification steps may not continue on error')
        for ref in FORBIDDEN_REFS:
            if ref in text:
                errors.append(f'{rel}: floating action reference {ref} is forbidden')
        for match in USES_RE.finditer(text):
            value = match.group(1)
            if value.startswith('./'):
                continue
            if '@' not in value:
                errors.append(f'{rel}: action without version: {value}')
                continue
            action, ref = value.rsplit('@', 1)
            if not SHA_RE.fullmatch(ref):
                errors.append(f'{rel}: action ref is not a full immutable SHA: {value}')
            used_actions.setdefault(action, set()).add(ref)
        if 'actions/checkout@' in text and 'persist-credentials: false' not in text:
            errors.append(f'{rel}: checkout must disable persisted credentials')
        if path.name in {'ci.yml', 'pages.yml', 'maintenance.yml'} and 'lake update' in text:
            errors.append(f'{rel}: verification workflows must not refresh the Lake lock')
        if 'leanprover/lean-action@' in text:
            for policy in (
                'auto-config: false',
                'build: true',
                'build-args: MarkedRootedClosure',
                'leanchecker: true',
            ):
                if policy not in text:
                    errors.append(f'{rel}: lean-action missing explicit policy: {policy}')
            duplicate_gate = re.compile(
                r'^\s*run:\s*make\s+(?:lean|verify|release)\s*$', re.MULTILINE
            )
            if duplicate_gate.search(text):
                errors.append(
                    f'{rel}: lean-action build must be followed by make lean-oracle, '
                    'not a second full Lean build'
                )
        if 'actions/setup-python@' in text:
            if 'cache-dependency-path: requirements-docs.lock' not in text:
                errors.append(f'{rel}: Python cache must key from requirements-docs.lock')
            if 'python -m pip install -r requirements-docs.lock' not in text:
                errors.append(f'{rel}: workflow must install requirements-docs.lock')
            if 'python -m pip install -r requirements-docs.txt' in text:
                errors.append(f'{rel}: workflow may not install the direct-only requirements file')
            if 'python -m pip check' not in text:
                errors.append(f'{rel}: workflow must run pip check after installing the lock')

    for action, refs in sorted(used_actions.items()):
        expected = expected_actions.get(action)
        if expected is None:
            errors.append(f'action missing from actions manifest: {action}')
        elif refs != {expected}:
            errors.append(f'action ref mismatch for {action}: expected {expected}, found {sorted(refs)}')
    unused = sorted(set(expected_actions) - set(used_actions))
    if unused:
        errors.append('actions manifest contains unused entries: ' + ', '.join(unused))

    ci = (workflows / 'ci.yml').read_text(encoding='utf-8')
    for needle in (
        'make verify-nonlean',
        'make package-determinism',
        'make smoke-release',
        'make lean-oracle',
    ):
        if needle not in ci:
            errors.append(f'ci.yml missing required command: {needle}')
    for suffix in ('*.spdx.json', '*.cdx.json', '*.buildinfo.json', '*.intoto.jsonl', '*.release.json', '*.checksums.sha256'):
        if suffix not in ci:
            errors.append(f'ci.yml does not upload {suffix}')

    project = load_project(root)
    guard = f"github.repository == '{repository_full_name(project)}'"
    pages = (workflows / 'pages.yml').read_text(encoding='utf-8')
    release = (workflows / 'release.yml').read_text(encoding='utf-8')
    maintenance = (workflows / 'maintenance.yml').read_text(encoding='utf-8')
    for name, text in (('ci.yml', ci), ('release.yml', release)):
        if 'use-github-cache: true' not in text:
            errors.append(f'{name} must enable the pinned Lean GitHub cache')
    for name, text in (('pages.yml', pages), ('release.yml', release), ('maintenance.yml', maintenance)):
        if guard not in text:
            errors.append(f'{name} must guard privileged work to the canonical repository')

    for suffix in ('*.zip', '*.sha256', '*.spdx.json', '*.cdx.json', '*.buildinfo.json', '*.intoto.jsonl', '*.release.json', '*.checksums.sha256'):
        if suffix not in release:
            errors.append(f'release.yml does not publish {suffix}')
    if '--verify-tag' not in release:
        errors.append('release.yml must verify the release tag')
    for needle in (
        'make lean-oracle',
        'make package-determinism',
        'use-github-cache: false',
    ):
        if needle not in maintenance:
            errors.append(f'maintenance.yml missing clean-room command/policy: {needle}')
    for needle in ('make lean-oracle', 'make package-determinism'):
        if needle not in release:
            errors.append(f'release.yml missing required command: {needle}')
    if 'make verify-nonlean' not in pages:
        errors.append('pages.yml must run the complete non-Lean verification target')
    return errors


def main() -> None:
    errors = validate(ROOT)
    if errors:
        raise SystemExit('Workflow audit failed:\n' + '\n'.join(f'- {e}' for e in errors))
    count = len([*WORKFLOWS.glob('*.yml'), *WORKFLOWS.glob('*.yaml')])
    print(f'workflow audit: OK ({count} workflows; immutable action SHAs enforced)')


if __name__ == '__main__':
    main()
