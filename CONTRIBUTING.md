# Contributing

Contributions should preserve the exact upstream lock and the paper's claim
boundary.  Every theorem change must include:

1. a Lean proof without `sorry`, `admit`, or a new axiom;
2. an oracle update;
3. a theorem-map update;
4. a paper update if the public statement changes;
5. a clean CI run.

Model-specific Yang-Mills assumptions must remain explicit and must not be
renamed as if proved by the finite combinatorial layer.
