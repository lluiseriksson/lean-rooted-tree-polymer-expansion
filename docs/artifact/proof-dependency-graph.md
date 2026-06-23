# Proof dependency graph

The public API is a deliberately small re-export layer over three theorem
endpoints in the pinned upstream development. The machine-readable graph is
[`archive/proof-dag.json`](https://github.com/lluiseriksson/lean-rooted-tree-polymer-expansion/blob/main/archive/proof-dag.json); its schema is
[`schemas/proof-dag.schema.json`](https://github.com/lluiseriksson/lean-rooted-tree-polymer-expansion/blob/main/schemas/proof-dag.schema.json).

```mermaid
flowchart LR
  U1[Rooted child-factorial profile bound]
  U2[Marked-root geometric leaf bound]
  U3[Target-preserving weighted-tree bound]
  P1[Public normalized profile endpoint]
  P2[Public marked-root endpoint]
  P3[Public target-preserving endpoint]

  U1 -->|combinatorial input| U2
  U2 -->|target-decay composition| U3
  U1 -->|re-exported as| P1
  U2 -->|re-exported as| P2
  U3 -->|re-exported as| P3
```

The graph is audited for unique nodes, valid source blob identities, direct
re-export edges, agreement with the theorem manifest, and acyclicity. It is a
traceability aid, not an independent proof object: the Lean kernel build and
axiom oracle remain authoritative.
