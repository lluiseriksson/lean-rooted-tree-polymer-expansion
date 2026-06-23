#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

python3 -m venv .venv-docs
.venv-docs/bin/python -m pip install --disable-pip-version-check -r requirements-docs.lock
.venv-docs/bin/python -m pip check
python3 scripts/check_lake_lock.py
python3 scripts/assemble_paper.py
printf '%s\n' "Bootstrap complete. The committed Lake manifest was not refreshed."
printf '%s\n' "Run locally: make verify-nonlean"
printf '%s\n' "Authoritative Lean gate: GitHub Actions; optional local gate: make lean"
