import re


def normalize(text: str) -> str:
    return " ".join(re.findall(r"\w+", text.casefold()))


def deduplicate(rows: list[dict]) -> list[dict]:
    seen = set()
    out = []
    for row in rows:
        key = normalize(row["query"])
        if len(key) < 8 or key in seen:
            continue
        seen.add(key)
        out.append(row)
    return out
