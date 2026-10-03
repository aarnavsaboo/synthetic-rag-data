# synthetic-rag-data

Local-model tooling for generating, organizing and analysing synthetic retrieval datasets.

The project turns a document collection into labelled retrieval queries using a language model running on the same machine. It is built as a pipeline rather than a single generation script: corpus ingestion, passage sampling, query generation, filtering, duplicate reduction, difficulty tagging, split assignment and corpus-coverage reporting are separate stages.

Synthetic data is useful for rapid RAG iteration because every generated query can inherit a relevance label from the passage it was generated from. It is not a substitute for real user queries, so the pipeline keeps provenance and synthetic/held-out splits explicit.

## Pipeline

```text
source corpus
    |
    v
passage sampler
    |
    v
local model generator
    |
    +--> direct questions
    +--> paraphrased questions
    +--> vague questions
    +--> multi-fact questions
    |
    v
normalization + deduplication
    |
    v
difficulty heuristics
    |
    v
stable split assignment
    |
    +--> train.jsonl
    +--> dev.jsonl
    +--> test.jsonl
    |
    v
coverage report
```

## Example

```bash
python -m synthetic_rag_data generate corpus.jsonl \
  --model qwen3:4b \
  --out runs/raw.jsonl \
  --questions 4

python -m synthetic_rag_data process runs/raw.jsonl \
  --out datasets/

python -m synthetic_rag_data report datasets/dev.jsonl
```

## Dataset records

Processed records keep:

- query text
- relevant source IDs
- generator model
- source passage ID
- generation mode
- approximate difficulty
- normalized query hash
- deterministic split
- source-length metadata

That makes it possible to reproduce retrieval experiments and inspect whether performance changes are concentrated in one synthetic query type.

## Generation modes

The included local generator can request several query styles:

- `direct` — explicit question using terms from the passage
- `paraphrase` — same information with different wording
- `underspecified` — fewer exact lexical clues
- `multi-fact` — requires combining two details from one passage

The styles are prompts, not guaranteed properties. They are stored as requested generation modes rather than claimed ground truth.

## Repository layout

- `corpus.py` — corpus loading and passage records
- `generator.py` — local generation interface
- `ollama.py` — localhost model adapter
- `filters.py` — normalization and duplicate reduction
- `difficulty.py` — lightweight descriptive features
- `splits.py` — stable dataset partitioning
- `pipeline.py` — stage orchestration
- `report.py` — coverage and distribution summaries
- `configs/` — pipeline manifests
- `tests/` — deterministic tests without model calls

Maintained by **Aarnav Saboo**.
