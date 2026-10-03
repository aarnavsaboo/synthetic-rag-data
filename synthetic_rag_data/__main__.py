from argparse import ArgumentParser
from pathlib import Path
import json

from .corpus import load, sample
from .io import read_jsonl, write_jsonl
from .ollama import OllamaQueryGenerator
from .pipeline import by_split, generate_rows
from .report import summarize


def main():
    parser = ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    gen = sub.add_parser("generate")
    gen.add_argument("corpus")
    gen.add_argument("--model", required=True)
    gen.add_argument("--out", required=True)
    gen.add_argument("--questions", type=int, default=3)
    gen.add_argument("--modes", nargs="+", default=["direct","paraphrase","underspecified"])
    gen.add_argument("--every", type=int, default=1)
    gen.add_argument("--max-source-chars", type=int)

    process = sub.add_parser("process")
    process.add_argument("path")
    process.add_argument("--out", required=True)

    report = sub.add_parser("report")
    report.add_argument("path")

    args = parser.parse_args()

    if args.cmd == "generate":
        passages = sample(load(args.corpus), args.every, args.max_source_chars)
        generator = OllamaQueryGenerator(args.model)
        rows = generate_rows(passages, generator, args.modes, args.questions)
        write_jsonl(args.out, rows)
        print(json.dumps(summarize(rows), indent=2))
    elif args.cmd == "process":
        rows = read_jsonl(args.path)
        root = Path(args.out)
        for split, values in by_split(rows).items():
            write_jsonl(str(root / f"{split}.jsonl"), values)
        print(json.dumps({"rows": len(rows), "splits": {k: len(v) for k, v in by_split(rows).items()}}, indent=2))
    else:
        print(json.dumps(summarize(read_jsonl(args.path)), indent=2))


if __name__ == "__main__":
    main()
