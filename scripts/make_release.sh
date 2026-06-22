#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
NAME="marked-rooted-closure-v1.0.0"
OUT="$ROOT/release"
STAGE="$OUT/$NAME"

rm -rf "$OUT"
mkdir -p "$STAGE"

rsync -a \
  --exclude '.git' \
  --exclude '.lake' \
  --exclude 'release' \
  --exclude 'paper/*.aux' \
  --exclude 'paper/*.bbl' \
  --exclude 'paper/*.blg' \
  --exclude 'paper/*.log' \
  --exclude 'paper/*.out' \
  --exclude 'paper/*.fls' \
  --exclude 'paper/*.fdb_latexmk' \
  --exclude 'paper/*.toc' \
  --exclude 'paper/*.synctex.gz' \
  --exclude 'paper/*.run.xml' \
  --exclude 'paper/graphical-abstract.pdf' \
  "$ROOT/" "$STAGE/"

(
  cd "$STAGE"
  find . -type f ! -name 'MANIFEST.sha256' -print0 \
    | LC_ALL=C sort -z \
    | xargs -0 sha256sum > MANIFEST.sha256
)

# Normalize timestamps so repeated releases from the same tree are stable.
find "$STAGE" -exec touch -t 202606221200.00 {} +

(
  cd "$OUT"
  LC_ALL=C find "$NAME" -type f -o -type d | LC_ALL=C sort \
    | zip -X -q "$NAME.zip" -@
  sha256sum "$NAME.zip" > "$NAME.zip.sha256"
)

echo "release created: $OUT/$NAME.zip"
