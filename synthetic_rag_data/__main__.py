from argparse import ArgumentParser
from pathlib import Path
import json

from .corpus import load
from .filters import deduplicate
from .ollama import questions


def main():
    parser = ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    gen = sub.add_parser("generate")
    gen.add_argument("corpus")
    gen.add_argument("--model", required=True)
    gen.add_argument("--out", required=True)
    gen.add_argument("--questions", type=int, default=3)
    args = parser.parse_args()

    rows = []
    for doc in load(args.corpus):
        for query in questions(args.model, doc["text"], args.questions):
            rows.append({"query": query, "relevant": [doc["id"]], "source": doc["id"]})
    rows = deduplicate(rows)
    target = Path(args.out)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in rows), encoding="utf-8")
    print(f"wrote {len(rows)} queries")


if __name__ == "__main__":
    main()
