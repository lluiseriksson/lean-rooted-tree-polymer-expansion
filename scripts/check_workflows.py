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
JOB_RE = re.compile(r'^  ([A-Za-z0-9_-]+):\s*$')
RELEASE_PUBLISH_SUFFIXES = (
    '.zip',
    '.spdx.json',
    '.cdx.json',
    '.buildinfo.json',
    '.intoto.jsonl',
    '.release.json',
    '.zip.sha256',
    '.spdx.json.sha256',
    '.cdx.json.sha256',
    '.buildinfo.json.sha256',
    '.intoto.jsonl.sha256',
    '.release.json.sha256',
    '.checksums.sha256',
)


def _job_block(text: str, name: str) -> str:
    """Return one top-level job block without requiring a YAML parser."""
    lines = text.splitlines(keepends=True)
    marker = f'  {name}:'
    start = next((index for index, line in enumerate(lines) if line.rstrip() == marker), None)
    if start is None:
        return ''
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if JOB_RE.fullmatch(lines[index].rstrip('\n')):
            end = index
            break
    return ''.join(lines[start:end])


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
    if 'name: source-package-preview' not in ci or 'path: release/' not in ci:
        errors.append('ci.yml must upload the already-verified exact release directory')

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

    release_prefix = release.split('\njobs:', 1)[0]
    verify_job = _job_block(release, 'verify-and-package')
    publish_job = _job_block(release, 'publish')
    if not verify_job or not publish_job:
        errors.append('release.yml must separate verify-and-package from publish')
    if 'permissions:\n  contents: read' not in release_prefix:
        errors.append('release.yml must default to read-only contents permission')
    if any(permission in release_prefix for permission in (
        'contents: write', 'id-token: write', 'attestations: write'
    )):
        errors.append('release.yml may not grant write/attestation permissions workflow-wide')
    for permission in ('contents: write', 'id-token: write', 'attestations: write'):
        if permission in verify_job:
            errors.append(f'release verify-and-package job may not grant {permission}')
        if permission not in publish_job:
            errors.append(f'release publish job must grant {permission}')
        if release.count(permission) != 1:
            errors.append(f'release.yml must grant {permission} exactly once')
    if 'needs: verify-and-package' not in publish_job:
        errors.append('release publish job must depend on verify-and-package')
    if "startsWith(github.ref, 'refs/tags/')" not in publish_job:
        errors.append('release publish job must be tag-only')
    if 'actions/upload-artifact@' not in verify_job or 'source-release-candidate' not in verify_job:
        errors.append('release verify job must stage source-release-candidate')
    if 'actions/download-artifact@' not in publish_job or 'source-release-candidate' not in publish_job:
        errors.append('release publish job must download source-release-candidate')
    if 'actions/checkout@' in publish_job:
        errors.append('release publish job must not checkout or execute repository code')
    if 'make ' in publish_job or 'scripts/' in publish_job:
        errors.append('release publish job must not execute repository build scripts')
    if 'Validate the exact release inventory' not in publish_job:
        errors.append('release publish job must validate the exact asset inventory')
    if 'release index artifact metadata mismatch' not in publish_job:
        errors.append('release publish job must bind release-index metadata to artifacts')
    if 'release/*' in publish_job:
        errors.append('release publish job may not use broad release asset globs')
    for suffix in RELEASE_PUBLISH_SUFFIXES:
        needle = 'release/${RELEASE_STEM}' + suffix
        if needle not in publish_job:
            errors.append(f'release publish job missing exact asset path: {needle}')
    if 'GH_TOKEN: ${{ github.token }}' not in publish_job:
        errors.append('release publish token must be scoped to the publication step')
    if '--verify-tag' not in publish_job:
        errors.append('release.yml must verify the release tag')
    if 'name: scheduled-release-evidence' not in maintenance or 'path: release/' not in maintenance:
        errors.append('maintenance.yml must upload the already-verified exact release directory')
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
