#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

python3 scripts/assemble_paper.py

if [[ -x .venv-docs/bin/python ]]; then
  PY=.venv-docs/bin/python
else
  PY=python3
fi

if ! "$PY" -c 'import mkdocs' >/dev/null 2>&1; then
  echo "MkDocs is not installed. Run: make docs-setup" >&2
  exit 2
fi

"$PY" -m mkdocs build --strict
