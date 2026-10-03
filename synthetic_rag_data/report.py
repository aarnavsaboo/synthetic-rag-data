from collections import Counter


def summarize(rows: list[dict]) -> dict:
    sources = {x["source_id"] for x in rows}
    modes = Counter(x["mode"] for x in rows)
    difficulties = Counter(x["difficulty"] for x in rows)
    overlaps = [float(x["features"]["lexical_overlap"]) for x in rows]
    return {
        "queries": len(rows),
        "unique_sources": len(sources),
        "modes": dict(sorted(modes.items())),
        "difficulty": dict(sorted(difficulties.items())),
        "mean_lexical_overlap": 0.0 if not overlaps else sum(overlaps) / len(overlaps),
    }
