from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class NoteMatch:
    path: Path
    score: int
    content: str


class MarkdownStore:
    """Simple local Markdown retrieval with no external search dependency."""

    def __init__(self, root: str | Path):
        self.root = Path(root)
        if not self.root.exists():
            raise FileNotFoundError(f"markdown root not found: {self.root}")

    def _files(self) -> Iterable[Path]:
        for path in self.root.rglob("*.md"):
            if any(part.startswith(".") for part in path.parts):
                continue
            yield path

    @staticmethod
    def _tokens(text: str) -> list[str]:
        return [
            token.lower()
            for token in re.findall(r"[A-Za-z0-9_.:/-]+", text)
            if len(token) >= 3
        ]

    def search(self, query: str, aliases: Iterable[str] = (), limit: int = 8) -> list[NoteMatch]:
        terms = set(self._tokens(query))
        for alias in aliases:
            terms.update(self._tokens(alias))
        if not terms:
            return []

        matches: list[NoteMatch] = []
        for path in self._files():
            try:
                content = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue

            haystack = content.lower()
            filename = path.stem.lower()
            score = 0
            for term in terms:
                if term in filename:
                    score += 6
                count = haystack.count(term)
                score += min(count, 5)
            if score:
                matches.append(NoteMatch(path=path, score=score, content=content))

        matches.sort(key=lambda item: (-item.score, str(item.path)))
        return matches[:limit]
