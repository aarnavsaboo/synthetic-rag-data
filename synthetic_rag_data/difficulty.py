from .filters import lexical_overlap, normalize


def features(query: str, passage: str) -> dict:
    query_tokens = normalize(query).split()
    passage_tokens = normalize(passage).split()
    overlap = lexical_overlap(query, passage)
    return {
        "query_tokens": len(query_tokens),
        "source_tokens_approx": len(passage_tokens),
        "lexical_overlap": overlap,
        "low_overlap": overlap < 0.35,
        "long_query": len(query_tokens) >= 18,
    }


def bucket(feature_row: dict) -> str:
    if feature_row["low_overlap"] and feature_row["long_query"]:
        return "harder"
    if feature_row["low_overlap"] or feature_row["long_query"]:
        return "medium"
    return "easier"
