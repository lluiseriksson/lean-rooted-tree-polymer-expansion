# Machine-readable project index

The site publishes a compact [`llms.txt`](../llms.txt) file for agents,
indexers, and automated artifact evaluators. It records the public theorem
endpoints, immutable proof pins, verification command, claims boundary, and the
highest-value repository paths.

The authoritative machine-readable records remain:

- [`project.json`](https://github.com/lluiseriksson/lean-rooted-tree-polymer-expansion/blob/main/project.json) for project identity and release metadata;
- [`archive/theorem-manifest.json`](https://github.com/lluiseriksson/lean-rooted-tree-polymer-expansion/blob/main/archive/theorem-manifest.json) for theorem provenance, source Git blobs, and signature fingerprints;
- [`archive/actions-manifest.json`](https://github.com/lluiseriksson/lean-rooted-tree-polymer-expansion/blob/main/archive/actions-manifest.json) for CI action dependencies;
- [`archive/proof-dag.json`](https://github.com/lluiseriksson/lean-rooted-tree-polymer-expansion/blob/main/archive/proof-dag.json) for the public proof dependency graph;
- [`requirements-docs.lock`](https://github.com/lluiseriksson/lean-rooted-tree-polymer-expansion/blob/main/requirements-docs.lock) for the exact transitive documentation environment;
- [`archive/UPSTREAM.lock`](https://github.com/lluiseriksson/lean-rooted-tree-polymer-expansion/blob/main/archive/UPSTREAM.lock) and [`lake-manifest.json`](https://github.com/lluiseriksson/lean-rooted-tree-polymer-expansion/blob/main/lake-manifest.json) for proof dependencies.

`llms.txt` is an index, not a substitute for the article, theorem statements,
or verification contract.

Generated releases add build-info schema v2, a release evidence index schema
v2, dual SBOMs, and a deterministic in-toto Statement v1 / SLSA declaration.
That local declaration records `executionBound: false`; tagged releases carry
separate hosted GitHub attestations as the execution-bound layer. These files
are generated evidence and are not tracked in the source tree.
