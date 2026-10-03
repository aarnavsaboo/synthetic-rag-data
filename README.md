# synthetic-rag-data

Generate small labelled retrieval datasets with a local language model.

The workflow takes source passages, asks a local model to produce realistic search questions, keeps the source passage ID as the relevance label, removes duplicate or near-empty questions, and exports JSONL that can be consumed by retrieval experiments.

The included adapter talks to Ollama on localhost. The dataset builder keeps generation separate from filtering so the raw model output can be inspected before it becomes an evaluation set.

```bash
python -m synthetic_rag_data generate corpus.jsonl \
  --model qwen3:4b \
  --out generated.jsonl
```

Synthetic queries are useful for iteration but should not replace a real held-out query set. A model can create questions that are much cleaner than the queries users actually write.

Maintained by **Aarnav Saboo**.
