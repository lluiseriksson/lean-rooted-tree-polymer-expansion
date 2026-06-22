#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

if ! command -v lake >/dev/null 2>&1; then
  echo "lake not found; install elan and the toolchain in lean-toolchain" >&2
  exit 2
fi

python3 -m venv .venv-docs
.venv-docs/bin/python -m pip install --disable-pip-version-check -r requirements-docs.txt
lake update
printf '%s\n' "Bootstrap complete. Run: make verify"
