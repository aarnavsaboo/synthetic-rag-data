# Workflow

Synthetic query generation is best used as a fast development loop:

1. freeze the source passages;
2. generate several queries per passage with a local model;
3. keep the raw generations;
4. remove empty and duplicate questions;
5. spot-check a sample;
6. evaluate retrieval;
7. repeat the final comparison on real queries.

The source passage ID becomes the relevance label automatically. That is convenient, but it can overstate retrieval quality when the generated question copies unusual vocabulary from the passage.
