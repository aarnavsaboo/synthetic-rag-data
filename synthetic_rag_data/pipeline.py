from __future__ import annotations

from collections import defaultdict

from .corpus import Passage
from .difficulty import bucket, features
from .filters import deduplicate
from .generator import QueryGenerator
from .splits import assign


def generate_rows(
    passages: list[Passage],
    generator: QueryGenerator,
    modes: list[str],
    questions_per_mode: int,
) -> list[dict]:
    source_lookup = {p.id: p for p in passages}
    raw = []
    for passage in passages:
        for mode in modes:
            for item in generator.generate(passage.id, passage.text, mode, questions_per_mode):
                raw.append({
                    "query": item.query,
                    "relevant": [item.source_id],
                    "source_id": item.source_id,
                    "generator_model": item.model,
                    "mode": item.mode,
                    "source_chars": item.source_chars,
                })

    processed = []
    for row in deduplicate(raw):
        passage = source_lookup[row["source_id"]]
        feature_row = features(row["query"], passage.text)
        processed.append({
            **row,
            "difficulty": bucket(feature_row),
            "features": feature_row,
            "split": assign(row["source_id"] + ":" + row["query_hash"]),
        })
    return processed


def by_split(rows: list[dict]) -> dict[str, list[dict]]:
    groups = defaultdict(list)
    for row in rows:
        groups[row["split"]].append(row)
    return dict(groups)
