#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

bad=0
while IFS= read -r file; do
  if grep -nE '(^|[[:space:]])(sorry|admit)([[:space:]]|$)|^[[:space:]]*axiom[[:space:]]' "$file"; then
    echo "placeholder found in $file" >&2
    bad=1
  fi
done < <(find . -path './.lake' -prune -o -name '*.lean' -type f -print)

if [[ "$bad" -ne 0 ]]; then
  exit 1
fi

echo "Lean source placeholder audit: clean"
