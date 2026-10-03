from pathlib import Path
import json


def load(path: str) -> list[dict]:
    rows = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            rows.append({"id": str(row["id"]), "text": str(row["text"])})
    return rows
