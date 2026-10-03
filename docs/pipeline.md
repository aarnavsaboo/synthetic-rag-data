# Pipeline notes

Synthetic retrieval data is most useful when it is treated as generated experiment material rather than as ground truth.

The pipeline preserves the source passage, requested generation mode and model identifier for every query. That allows later retrieval reports to answer questions such as:

- did a new embedding model mostly improve low-overlap queries?
- did reranking help the underspecified subset but hurt direct queries?
- is one source passage producing an unusually large fraction of failures?
- does a held-out split behave differently from the generated training split?

Stable split assignment uses a hash rather than input order, so adding new records does not reshuffle the entire dataset.
