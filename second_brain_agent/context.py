from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .db import Relationship, StateDatabase
from .markdown import MarkdownStore, NoteMatch


STOP_WORDS = {
    "about", "after", "again", "against", "also", "because", "before",
    "between", "could", "from", "have", "into", "just", "more", "need",
    "please", "show", "that", "their", "there", "these", "they", "this",
    "using", "want", "what", "when", "where", "which", "with", "would",
}


@dataclass(frozen=True)
class ContextBundle:
    prompt: str
    entities: list[str]
    relationships: list[Relationship]
    notes: list[NoteMatch]

    def as_markdown(self, max_chars_per_note: int = 5000) -> str:
        lines = ["# Retrieved second-brain context", "", "## Query", self.prompt, ""]

        if self.entities:
            lines.extend(["## Matched entities", *[f"- {e}" for e in self.entities], ""])

        if self.relationships:
            lines.append("## Knowledge-graph relationships")
            for edge in self.relationships:
                lines.append(f"- {edge.source} --{edge.relation}--> {edge.target}")
            lines.append("")

        if self.notes:
            lines.append("## Relevant notes")
            for note in self.notes:
                lines.extend(
                    [
                        f"### {note.path}",
                        note.content[:max_chars_per_note],
                        "",
                    ]
                )

        return "\n".join(lines).strip() + "\n"


class ContextBuilder:
    """Retrieve graph relationships and Markdown context for a natural-language prompt."""

    def __init__(self, db_path: str | Path, markdown_root: str | Path):
        self.db = StateDatabase(db_path)
        self.notes = MarkdownStore(markdown_root)

    @staticmethod
    def prompt_terms(prompt: str, limit: int = 12) -> list[str]:
        tokens = [
            token.lower()
            for token in re.findall(r"[A-Za-z0-9_.:/-]+", prompt)
            if len(token) >= 3
        ]
        result: list[str] = []
        for token in tokens:
            if token in STOP_WORDS or token in result:
                continue
            result.append(token)
            if len(result) >= limit:
                break
        return result

    def build(self, prompt: str, note_limit: int = 8, relationship_limit: int = 80) -> ContextBundle:
        terms = self.prompt_terms(prompt)
        entities = self.db.find_nodes(terms)

        # If the nodes table is absent or sparse, prompt terms still act as graph aliases.
        relationship_aliases = list(entities) + terms
        relationships: list[Relationship] = []
        seen_edges: set[tuple[str, str, str]] = set()

        for alias in relationship_aliases:
            for edge in self.db.relationships_for(alias, limit=relationship_limit):
                key = (edge.source, edge.relation, edge.target)
                if key in seen_edges:
                    continue
                seen_edges.add(key)
                relationships.append(edge)
                if len(relationships) >= relationship_limit:
                    break
            if len(relationships) >= relationship_limit:
                break

        graph_names: list[str] = []
        for edge in relationships:
            graph_names.extend([edge.source, edge.target])
        aliases = list(dict.fromkeys([*entities, *graph_names]))

        notes = self.notes.search(prompt, aliases=aliases, limit=note_limit)
        return ContextBundle(
            prompt=prompt,
            entities=entities,
            relationships=relationships,
            notes=notes,
        )
