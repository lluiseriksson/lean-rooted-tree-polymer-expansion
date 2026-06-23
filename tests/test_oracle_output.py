from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

from check_oracle_output import (  # noqa: E402
    EXPECTED_AXIOMS,
    PUBLIC_THEOREMS,
    parse_axioms,
    validate_oracle_output,
)


def valid_log() -> str:
    return '\n'.join(
        f"'{name}' depends on axioms: [propext, Classical.choice, Quot.sound]"
        for name in PUBLIC_THEOREMS
    )


class OracleOutputTests(unittest.TestCase):
    def test_parses_exact_axioms(self) -> None:
        self.assertEqual(parse_axioms(valid_log(), PUBLIC_THEOREMS[0]), EXPECTED_AXIOMS)

    def test_valid_log_passes(self) -> None:
        self.assertEqual(validate_oracle_output(valid_log()), [])

    def test_extra_axiom_fails(self) -> None:
        text = valid_log().replace(
            'Quot.sound]', 'Quot.sound, project.localAxiom]', 1
        )
        errors = validate_oracle_output(text)
        self.assertTrue(any('extra=project.localAxiom' in error for error in errors))

    def test_missing_theorem_report_fails(self) -> None:
        text = '\n'.join(valid_log().splitlines()[:-1])
        errors = validate_oracle_output(text)
        self.assertTrue(any('axiom report missing' in error for error in errors))

    def test_forbidden_sorry_ax_fails(self) -> None:
        errors = validate_oracle_output(valid_log() + '\nsorryAx\n')
        self.assertTrue(any('sorryAx' in error for error in errors))


if __name__ == '__main__':
    unittest.main()
