/- Copyright (c) 2026 Lluis Eriksson.
SPDX-License-Identifier: AGPL-3.0-or-later -/

import MarkedRootedClosure.PaperTheorems

/-!
Run with:

```bash
lake env lean MarkedRootedClosure/Oracle.lean
```

The output should list only the standard classical axioms inherited from
Mathlib and the pinned upstream proof development.
-/

#print axioms MarkedRootedClosure.normalizedRootedChildFactorialTreeBound
#print axioms MarkedRootedClosure.markedRootLeafGeometricBound
#print axioms MarkedRootedClosure.targetPreservingWeightedTreeBound
