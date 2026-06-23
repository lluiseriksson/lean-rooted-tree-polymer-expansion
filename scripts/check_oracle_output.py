#!/usr/bin/env python3
"""Require the exact documented axiom set for every public Lean endpoint."""
from __future__ import annotations

import re
import sys
from pathlib import Path

PUBLIC_THEOREMS = (
    'normalizedRootedChildFactorialTreeBound',
    'markedRootLeafGeometricBound',
    'targetPreservingWeightedTreeBound',
)
EXPECTED_AXIOMS = frozenset({'propext', 'Classical.choice', 'Quot.sound'})
FORBIDDEN_TOKENS = ('sorryAx', 'admit', 'unsound', 'Lean.ofReduceBool')


def _normalise_axiom_token(token: str) -> str:
    token = token.strip().strip("'`\"")
    token = token.removeprefix('axiom ')
    return token.strip()


def parse_axioms(text: str, theorem: str) -> frozenset[str]:
    qualified = rf"(?:MarkedRootedClosure\.)?{re.escape(theorem)}"
    # Lean normally prints: 'name' depends on axioms: [a, b, c]
    pattern = re.compile(
        rf"['«]?{qualified}['»]?\s+depends\s+on\s+axioms\s*:\s*\[([^\]]*)\]",
        re.IGNORECASE | re.DOTALL,
    )
    match = pattern.search(text)
    if match is None:
        raise ValueError(f'axiom report missing for theorem: {theorem}')
    raw = match.group(1)
    tokens = [_normalise_axiom_token(item) for item in raw.split(',')]
    return frozenset(token for token in tokens if token)


def validate_oracle_output(text: str) -> list[str]:
    errors: list[str] = []
    for forbidden in FORBIDDEN_TOKENS:
        if forbidden in text:
            errors.append(f'forbidden oracle dependency found: {forbidden}')
    for theorem in PUBLIC_THEOREMS:
        try:
            axioms = parse_axioms(text, theorem)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if axioms != EXPECTED_AXIOMS:
            missing = sorted(EXPECTED_AXIOMS - axioms)
            extra = sorted(axioms - EXPECTED_AXIOMS)
            detail: list[str] = []
            if missing:
                detail.append('missing=' + ','.join(missing))
            if extra:
                detail.append('extra=' + ','.join(extra))
            errors.append(f'{theorem}: unexpected axiom set ({"; ".join(detail)})')
    return errors


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit('usage: check_oracle_output.py PATH_TO_ORACLE_LOG')
    text = Path(sys.argv[1]).read_text(encoding='utf-8', errors='replace')
    errors = validate_oracle_output(text)
    if errors:
        raise SystemExit('oracle output audit failed:\n' + '\n'.join(f'- {e}' for e in errors))
    print('oracle output audit: OK (exact classical axiom set for 3 endpoints)')


if __name__ == '__main__':
    main()
