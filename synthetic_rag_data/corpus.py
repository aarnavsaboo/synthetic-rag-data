from dataclasses import dataclass
from pathlib import Path
import json


@dataclass(frozen=True)
class Passage:
    id: str
    text: str
    metadata: dict


def load(path: str) -> list[Passage]:
    rows = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        rows.append(Passage(
            id=str(row["id"]),
            text=str(row["text"]),
            metadata=dict(row.get("metadata", {})),
        ))
    return rows


def sample(passages: list[Passage], every: int = 1, max_chars: int | None = None) -> list[Passage]:
    if every < 1:
        raise ValueError("every must be >= 1")
    out = passages[::every]
    if max_chars is not None:
        out = [Passage(x.id, x.text[:max_chars], x.metadata) for x in out]
    return out
