#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

lake update
lake build MarkedRootedClosure
lake env lean MarkedRootedClosure/Oracle.lean
bash scripts/build_docs.sh
bash scripts/check_no_placeholders.sh
python3 scripts/check_artifact.py
python3 scripts/check_internal_links.py
