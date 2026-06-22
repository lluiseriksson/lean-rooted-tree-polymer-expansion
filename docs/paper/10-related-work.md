# Related work and novelty boundary

Tree-graph identities and polymer expansions have a long history
(Penrose 1967; Brydges 1986; Kotecký and Preiss 1986; Fernández and
Procacci 2007). Degree profiles, weak compositions, and central binomial
estimates are classical enumerative tools (Stanley 2012; Flajolet and
Sedgewick 2009). The Balaban--Dimock program supplies the source-facing
context in which connected polymers with holes, modified metrics, and
repeated cluster expansions occur (Dimock 2013a, 2013b, 2014).

The formalization does not claim a new classical tree-graph identity.
Its contribution is the machine-checked assembly of a particular proof
pipeline in which several superficially harmless reorderings are invalid
for the target-sensitive conclusion. In particular:

- the target is not replaced by a global sum before target decay is
  extracted;

- the tree is not replaced by independent vertex weights before
  parent--child moment summation;

- the parent-dependent moment factor is normalized and canceled exactly
  rather than bounded globally;

- the $(n+1)$ marking factor is canceled by the Ursell normalization and
  the rooted tree-profile estimate, not absorbed into an unspecified
  constant.

To the best of our knowledge, no prior Lean artifact formalizes this
exact target-preserving with-holes second-Ursell leaf-summation
pipeline. This is a scoped literature statement, not a claim of priority
over all formal or informal cluster-expansion arguments.
