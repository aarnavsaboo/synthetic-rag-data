# Limitations

A local model can generate queries that are cleaner, more grammatical and more directly answerable than real search traffic. It can also reuse terminology from the passage, making lexical retrieval look artificially strong.

The `difficulty` field is a descriptive heuristic based on query length and lexical overlap. It is not a claim about human difficulty.

Use synthetic queries for pipeline development and ablations. Keep a separate set of real or manually written queries for final comparisons.
