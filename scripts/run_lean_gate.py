#!/usr/bin/env python3
"""Run the local Lean build/oracle gate under a process-tree supervisor."""
from __future__ import annotations

import argparse
import os
import subprocess
from pathlib import Path

from check_oracle_output import validate_oracle_output
from process_runner import (
    CommandInterrupted,
    CommandTimedOut,
    ParentProcessExited,
    run_checked,
)
from project_config import ROOT

DEFAULT_BUILD_TIMEOUT = 3600
DEFAULT_ORACLE_TIMEOUT = 600


def _positive_seconds(value: str) -> float:
    try:
        seconds = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"not a number: {value!r}") from exc
    if seconds <= 0:
        raise argparse.ArgumentTypeError("timeout must be positive")
    return seconds


def _manifest_bytes(root: Path) -> bytes:
    path = root / "lake-manifest.json"
    try:
        return path.read_bytes()
    except OSError as exc:
        raise RuntimeError(f"cannot snapshot {path}: {exc}") from exc


def _require_manifest_unchanged(root: Path, before: bytes) -> None:
    after = _manifest_bytes(root)
    if after != before:
        raise RuntimeError(
            "lake-manifest.json changed during verification; restore and review the lock"
        )


def run_build(root: Path, *, lake: str, timeout: float) -> None:
    before = _manifest_bytes(root)
    print(f"Lean build supervisor: timeout={timeout:g}s", flush=True)
    run_checked(
        [lake, "build", "MarkedRootedClosure"],
        cwd=root,
        timeout=timeout,
    )
    _require_manifest_unchanged(root, before)
    print("Lean build gate: OK", flush=True)


def run_oracle(
    root: Path, *, lake: str, timeout: float, oracle_log: Path
) -> None:
    before = _manifest_bytes(root)
    print(f"Lean oracle supervisor: timeout={timeout:g}s", flush=True)
    completed = run_checked(
        [lake, "env", "lean", "MarkedRootedClosure/Oracle.lean"],
        cwd=root,
        timeout=timeout,
        tee_path=oracle_log,
    )
    _require_manifest_unchanged(root, before)
    text = completed.stdout or oracle_log.read_text(encoding="utf-8", errors="replace")
    errors = validate_oracle_output(text)
    if errors:
        raise RuntimeError(
            "oracle output audit failed:\n" + "\n".join(f"- {error}" for error in errors)
        )
    oracle_log.unlink(missing_ok=True)
    print("oracle output audit: OK (exact classical axiom set for 3 endpoints)", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("build", "oracle", "all"))
    parser.add_argument(
        "--build-timeout",
        type=_positive_seconds,
        default=_positive_seconds(os.environ.get("LEAN_BUILD_TIMEOUT", str(DEFAULT_BUILD_TIMEOUT))),
    )
    parser.add_argument(
        "--oracle-timeout",
        type=_positive_seconds,
        default=_positive_seconds(os.environ.get("LEAN_ORACLE_TIMEOUT", str(DEFAULT_ORACLE_TIMEOUT))),
    )
    parser.add_argument("--oracle-log", type=Path, default=Path(".oracle.log"))
    parser.add_argument("--lake", default=os.environ.get("LAKE", "lake"))
    args = parser.parse_args()

    oracle_log = args.oracle_log
    if not oracle_log.is_absolute():
        oracle_log = ROOT / oracle_log
    try:
        if args.mode in {"build", "all"}:
            run_build(ROOT, lake=args.lake, timeout=args.build_timeout)
        if args.mode in {"oracle", "all"}:
            run_oracle(
                ROOT,
                lake=args.lake,
                timeout=args.oracle_timeout,
                oracle_log=oracle_log,
            )
    except (
        CommandTimedOut,
        ParentProcessExited,
        CommandInterrupted,
        subprocess.CalledProcessError,
        RuntimeError,
        OSError,
    ) as exc:
        if args.mode in {"oracle", "all"} and oracle_log.exists():
            raise SystemExit(f"{exc}\npartial oracle log retained at {oracle_log}") from exc
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    main()
