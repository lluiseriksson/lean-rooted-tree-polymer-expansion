from __future__ import annotations

import os
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from run_lean_gate import run_build, run_oracle  # noqa: E402


VALID_ORACLE = "\n".join(
    f"'{name}' depends on axioms: [propext, Classical.choice, Quot.sound]"
    for name in (
        "normalizedRootedChildFactorialTreeBound",
        "markedRootLeafGeometricBound",
        "targetPreservingWeightedTreeBound",
    )
)


def _fake_lake(root: Path, oracle: str = VALID_ORACLE, *, drift: bool = False) -> Path:
    script = root / "fake-lake.py"
    drift_code = (
        "Path('lake-manifest.json').write_text('changed\\n', encoding='utf-8')"
        if drift
        else "pass"
    )
    script.write_text(
        textwrap.dedent(
            f"""\
            #!{sys.executable}
            import sys
            from pathlib import Path

            args = sys.argv[1:]
            if args == ["build", "MarkedRootedClosure"]:
                {drift_code}
                print("fake Lean build complete")
                raise SystemExit(0)
            if args == ["env", "lean", "MarkedRootedClosure/Oracle.lean"]:
                print({oracle!r})
                raise SystemExit(0)
            raise SystemExit(9)
            """
        ),
        encoding="utf-8",
    )
    script.chmod(0o755)
    if os.name == "nt":
        launcher = root / "fake-lake.cmd"
        launcher.write_text(
            f'@echo off\r\n"{sys.executable}" "{script}" %*\r\n',
            encoding="utf-8",
        )
        return launcher
    return script


class LeanGateTests(unittest.TestCase):
    def _root(self, temp: str) -> Path:
        root = Path(temp)
        (root / "lake-manifest.json").write_text('{"version": 7}\n', encoding="utf-8")
        (root / "MarkedRootedClosure").mkdir()
        (root / "MarkedRootedClosure" / "Oracle.lean").write_text("#print axioms\n", encoding="utf-8")
        return root

    def test_build_and_oracle_succeed_without_lock_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = self._root(temp)
            lake = _fake_lake(root)
            log = root / ".oracle.log"
            run_build(root, lake=str(lake), timeout=5)
            run_oracle(root, lake=str(lake), timeout=5, oracle_log=log)
            self.assertFalse(log.exists())
            self.assertEqual(
                (root / "lake-manifest.json").read_text(encoding="utf-8"),
                '{"version": 7}\n',
            )

    def test_oracle_failure_retains_log(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = self._root(temp)
            invalid = VALID_ORACLE.replace(
                "Quot.sound]", "Quot.sound, project.localAxiom]", 1
            )
            lake = _fake_lake(root, invalid)
            log = root / ".oracle.log"
            with self.assertRaisesRegex(RuntimeError, "unexpected axiom set"):
                run_oracle(root, lake=str(lake), timeout=5, oracle_log=log)
            self.assertTrue(log.is_file())
            self.assertIn("project.localAxiom", log.read_text(encoding="utf-8"))

    def test_build_rejects_lake_manifest_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = self._root(temp)
            lake = _fake_lake(root, drift=True)
            with self.assertRaisesRegex(RuntimeError, "lake-manifest.json changed"):
                run_build(root, lake=str(lake), timeout=5)


if __name__ == "__main__":
    unittest.main()
