from urllib.request import Request, urlopen
import json


def questions(model: str, passage: str, count: int = 3, endpoint: str = "http://127.0.0.1:11434") -> list[str]:
    prompt = f"""Write {count} short search questions that can be answered directly from the passage.
Return only a JSON array of strings.

PASSAGE:
{passage}
"""
    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {"temperature": 0.6},
    }).encode()
    req = Request(endpoint.rstrip("/") + "/api/generate", data=payload,
                  headers={"Content-Type":"application/json"}, method="POST")
    with urlopen(req, timeout=600) as response:
        outer = json.load(response)
    data = json.loads(outer["response"])
    if isinstance(data, dict):
        data = data.get("questions", [])
    return [str(x).strip() for x in data if str(x).strip()]
