from __future__ import annotations

from urllib.request import Request, urlopen
import json

from .generator import GeneratedQuery


INSTRUCTIONS = {
    "direct": "Write short search questions that can be answered directly from the passage. Preserve useful terminology.",
    "paraphrase": "Write search questions answerable from the passage but avoid copying its distinctive wording.",
    "underspecified": "Write plausible short user questions with fewer exact lexical clues while remaining answerable from the passage.",
    "multi-fact": "Write questions that require combining at least two details stated in the passage.",
}


class OllamaQueryGenerator:
    def __init__(self, model: str, endpoint: str = "http://127.0.0.1:11434"):
        self.model = model
        self.endpoint = endpoint.rstrip("/")

    def generate(self, source_id: str, passage: str, mode: str, count: int) -> list[GeneratedQuery]:
        if mode not in INSTRUCTIONS:
            raise ValueError(f"unknown generation mode: {mode}")
        prompt = f"""{INSTRUCTIONS[mode]}
Return only a JSON object with a single key "questions" containing an array of {count} strings.

PASSAGE:
{passage}
"""
        body = json.dumps({
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": {"temperature": 0.65},
        }).encode()
        request = Request(
            self.endpoint + "/api/generate",
            data=body,
            headers={"Content-Type":"application/json"},
            method="POST",
        )
        with urlopen(request, timeout=600) as response:
            outer = json.load(response)
        parsed = json.loads(outer["response"])
        values = parsed.get("questions", []) if isinstance(parsed, dict) else []
        return [
            GeneratedQuery(
                query=str(value).strip(),
                source_id=source_id,
                model=self.model,
                mode=mode,
                source_chars=len(passage),
            )
            for value in values
            if str(value).strip()
        ]
