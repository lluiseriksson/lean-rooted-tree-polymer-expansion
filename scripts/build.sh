#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
lake update
lake build MarkedRootedClosure
lake env lean MarkedRootedClosure/Oracle.lean
make -C paper clean all
bash scripts/check_no_placeholders.sh
python3 scripts/check_artifact.py
