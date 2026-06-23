from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

from lean_signatures import extract_theorem_signature, signature_sha256  # noqa: E402


class LeanSignatureTests(unittest.TestCase):
    def test_extracts_statement_without_proof(self) -> None:
        text = '''
/- doc comment with := noise -/
theorem sample {α : Type} (x : α) : x = x := by
  rfl
'''
        self.assertEqual(
            extract_theorem_signature(text, 'sample'),
            'theorem sample {α : Type} (x : α) : x = x',
        )

    def test_ignores_nested_comments_and_line_comments(self) -> None:
        text = '''
theorem sample
    (x : Nat) -- line comment
    /- outer /- inner -/ comment -/
    : x + 0 = x := by
  simp
'''
        self.assertEqual(
            extract_theorem_signature(text, 'sample'),
            'theorem sample (x : Nat) : x + 0 = x',
        )

    def test_fingerprint_is_whitespace_stable(self) -> None:
        a = 'theorem t (x : Nat) : x = x := by rfl\n'
        b = 'theorem   t\n  (x : Nat)\n  : x = x := by\n  rfl\n'
        self.assertEqual(signature_sha256(a, 't'), signature_sha256(b, 't'))

    def test_public_wrapper_signatures_are_unique(self) -> None:
        path = ROOT / 'MarkedRootedClosure' / 'PaperTheorems.lean'
        text = path.read_text(encoding='utf-8')
        names = [
            'normalizedRootedChildFactorialTreeBound',
            'markedRootLeafGeometricBound',
            'targetPreservingWeightedTreeBound',
        ]
        hashes = [signature_sha256(text, name) for name in names]
        self.assertEqual(len(hashes), len(set(hashes)))


if __name__ == '__main__':
    unittest.main()
