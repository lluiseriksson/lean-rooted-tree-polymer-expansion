#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: $0 <git-remote-url>" >&2
  exit 2
fi

REMOTE="$1"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ -d .git ]]; then
  echo "repository already initialized" >&2
  exit 1
fi

git init -b main
git add .
git commit -m "release: publication artifact v1.0.0"
git remote add origin "$REMOTE"

echo "initialized repository with remote: $REMOTE"
echo "next: git push -u origin main"
