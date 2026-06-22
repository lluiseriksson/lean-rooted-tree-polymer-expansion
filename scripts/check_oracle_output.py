#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

if len(sys.argv) != 2:
    raise SystemExit("usage: check_oracle_output.py PATH_TO_ORACLE_LOG")
text = Path(sys.argv[1]).read_text(encoding="utf-8", errors="replace")
required = [
    "normalizedRootedChildFactorialTreeBound",
    "markedRootLeafGeometricBound",
    "targetPreservingWeightedTreeBound",
]
missing = [name for name in required if name not in text]
if missing:
    raise SystemExit("oracle output is missing theorem names: " + ", ".join(missing))
for forbidden in ("sorryAx", "admit", "unsound", "Lean.ofReduceBool"):
    if forbidden in text:
        raise SystemExit(f"forbidden oracle dependency found: {forbidden}")
print("oracle output audit: OK")
