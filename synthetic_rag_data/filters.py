from hashlib import sha1
import re


def normalize(text: str) -> str:
    return " ".join(re.findall(r"\w+", text.casefold(), flags=re.UNICODE))


def query_hash(text: str) -> str:
    return sha1(normalize(text).encode()).hexdigest()[:16]


def deduplicate(rows: list[dict], min_normalized_chars: int = 8) -> list[dict]:
    seen = set()
    out = []
    for row in rows:
        key = normalize(row["query"])
        if len(key) < min_normalized_chars or key in seen:
            continue
        seen.add(key)
        copy = dict(row)
        copy["query_hash"] = query_hash(row["query"])
        out.append(copy)
    return out


def lexical_overlap(query: str, passage: str) -> float:
    q = set(normalize(query).split())
    p = set(normalize(passage).split())
    return 0.0 if not q else len(q & p) / len(q)
