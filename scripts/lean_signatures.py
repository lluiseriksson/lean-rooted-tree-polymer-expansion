#!/usr/bin/env python3
"""Extract and fingerprint public Lean theorem declarations.

This intentionally implements only the small declaration grammar used by the
publication wrapper.  It ignores proof terms and hashes a whitespace-normalized
statement from ``theorem NAME`` through the declaration's first top-level ``:=``
or ``:= by`` marker.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

THEOREM_START = re.compile(r"(?m)^theorem\s+([A-Za-z_][A-Za-z0-9_']*)\b")


def strip_comments(text: str) -> str:
    """Remove nested Lean block comments and line comments, preserving strings."""
    out: list[str] = []
    i = 0
    depth = 0
    in_string = False
    escaped = False
    while i < len(text):
        if depth:
            if text.startswith('/-', i):
                depth += 1
                i += 2
            elif text.startswith('-/', i):
                depth -= 1
                i += 2
            else:
                i += 1
            continue
        ch = text[i]
        if in_string:
            out.append(ch)
            if escaped:
                escaped = False
            elif ch == '\\':
                escaped = True
            elif ch == '"':
                in_string = False
            i += 1
            continue
        if ch == '"':
            in_string = True
            out.append(ch)
            i += 1
        elif text.startswith('/-', i):
            depth = 1
            i += 2
        elif text.startswith('--', i):
            newline = text.find('\n', i)
            if newline == -1:
                break
            out.append('\n')
            i = newline + 1
        else:
            out.append(ch)
            i += 1
    if depth:
        raise ValueError("unterminated Lean block comment")
    if in_string:
        raise ValueError("unterminated Lean string literal")
    return ''.join(out)


def _find_proof_marker(text: str, start: int) -> int:
    """Return the start of the first declaration-level ``:=`` after ``start``."""
    paren = bracket = brace = 0
    in_string = False
    escaped = False
    i = start
    while i < len(text) - 1:
        ch = text[i]
        if in_string:
            if escaped:
                escaped = False
            elif ch == '\\':
                escaped = True
            elif ch == '"':
                in_string = False
            i += 1
            continue
        if ch == '"':
            in_string = True
        elif ch == '(':
            paren += 1
        elif ch == ')':
            paren -= 1
        elif ch == '[':
            bracket += 1
        elif ch == ']':
            bracket -= 1
        elif ch == '{':
            brace += 1
        elif ch == '}':
            brace -= 1
        elif text.startswith(':=', i) and paren == bracket == brace == 0:
            return i
        if min(paren, bracket, brace) < 0:
            raise ValueError("unbalanced delimiter while parsing Lean declaration")
        i += 1
    raise ValueError("Lean theorem declaration has no top-level := proof marker")


def extract_theorem_signature(text: str, theorem_name: str) -> str:
    clean = strip_comments(text)
    match = next((m for m in THEOREM_START.finditer(clean) if m.group(1) == theorem_name), None)
    if match is None:
        raise KeyError(f"theorem not found: {theorem_name}")
    end = _find_proof_marker(clean, match.end())
    declaration = clean[match.start():end].strip()
    # Whitespace normalization makes the fingerprint insensitive to formatting,
    # while preserving every token in the theorem statement.
    return ' '.join(declaration.split())


def signature_sha256(text: str, theorem_name: str) -> str:
    canonical = extract_theorem_signature(text, theorem_name)
    return hashlib.sha256(canonical.encode('utf-8')).hexdigest()


def signature_sha256_file(path: Path, theorem_name: str) -> str:
    return signature_sha256(path.read_text(encoding='utf-8'), theorem_name)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=Path)
    parser.add_argument('theorem', nargs='+')
    args = parser.parse_args()
    content = args.path.read_text(encoding='utf-8')
    for name in args.theorem:
        print(f"{name}  {signature_sha256(content, name)}")
