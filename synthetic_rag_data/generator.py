from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class GeneratedQuery:
    query: str
    source_id: str
    model: str
    mode: str
    source_chars: int


class QueryGenerator(Protocol):
    model: str

    def generate(self, source_id: str, passage: str, mode: str, count: int) -> list[GeneratedQuery]: ...
