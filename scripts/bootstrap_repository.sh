#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

if ! command -v lake >/dev/null 2>&1; then
  echo "lake not found; install elan and the toolchain named in lean-toolchain" >&2
  exit 2
fi

python3 -m venv .venv-docs
.venv-docs/bin/python -m pip install --disable-pip-version-check -r requirements-docs.lock
.venv-docs/bin/python -m pip check
python3 scripts/check_lake_lock.py
python3 scripts/assemble_paper.py
printf '%s\n' "Bootstrap complete. The committed Lake manifest was not refreshed."
printf '%s\n' "Run: make verify"
