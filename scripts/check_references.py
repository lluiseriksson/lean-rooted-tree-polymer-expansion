#!/usr/bin/env python3
"""Cross-check the canonical BibTeX file against the rendered references page."""
from __future__ import annotations

import re
from pathlib import Path

from project_config import ROOT

ENTRY_RE = re.compile(r"@\w+\s*\{\s*([^,\s]+)\s*,", re.IGNORECASE)
FIELD_RE = re.compile(r"(?mi)^\s*(doi|eprint|url)\s*=\s*\{([^}]*)\}")
NUMBERED_REF_RE = re.compile(r"(?m)^(\d+)\.[ \t]+")


def bib_entries(text: str) -> list[tuple[str, str]]:
    starts = list(ENTRY_RE.finditer(text))
    entries: list[tuple[str, str]] = []
    for i, match in enumerate(starts):
        end = starts[i + 1].start() if i + 1 < len(starts) else len(text)
        entries.append((match.group(1), text[match.start():end]))
    return entries


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    bib_path = root / 'docs' / 'paper' / 'references.bib'
    rendered_path = root / 'docs' / 'paper' / 'references.md'
    bib = bib_path.read_text(encoding='utf-8')
    rendered = rendered_path.read_text(encoding='utf-8')
    entries = bib_entries(bib)
    keys = [key for key, _ in entries]
    if not entries:
        errors.append('references.bib has no entries')
    if len(keys) != len(set(keys)):
        errors.append('references.bib contains duplicate keys')
    numbered = [int(value) for value in NUMBERED_REF_RE.findall(rendered)]
    if numbered != list(range(1, len(entries) + 1)):
        errors.append(
            f'references.md numbering/count mismatch: expected {len(entries)} sequential entries'
        )
    for key, entry in entries:
        fields = {name.lower(): value.strip() for name, value in FIELD_RE.findall(entry)}
        doi = fields.get('doi')
        if doi and f'https://doi.org/{doi}' not in rendered:
            errors.append(f'rendered references missing DOI for {key}: {doi}')
        eprint = fields.get('eprint')
        if eprint and f'https://arxiv.org/abs/{eprint}' not in rendered:
            errors.append(f'rendered references missing arXiv link for {key}: {eprint}')
        url = fields.get('url')
        if url and url not in rendered:
            errors.append(f'rendered references missing URL for {key}: {url}')
    if '[BibTeX source](references.bib)' not in rendered:
        errors.append('references.md must link to the canonical BibTeX source')
    return errors


def main() -> None:
    errors = validate(ROOT)
    if errors:
        raise SystemExit('reference audit failed:\n' + '\n'.join(f'- {e}' for e in errors))
    count = len(bib_entries((ROOT / 'docs/paper/references.bib').read_text(encoding='utf-8')))
    print(f'reference audit: OK ({count} BibTeX entries)')


if __name__ == '__main__':
    main()
