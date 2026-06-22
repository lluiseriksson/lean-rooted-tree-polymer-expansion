#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PDF="$ROOT/paper/main.pdf"

pdfinfo "$PDF" | grep -q '^Pages:[[:space:]]*16$'
pdffonts "$PDF" | tail -n +3 | awk '{ if ($5 != "yes") bad=1 } END { exit bad }'

if grep -q 'Overfull \\hbox' "$ROOT/paper/main.log" 2>/dev/null; then
  echo "LaTeX overfull box detected" >&2
  exit 1
fi

echo "PDF preflight: 16 pages, embedded fonts, no overfull boxes"
