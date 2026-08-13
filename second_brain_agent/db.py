from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Relationship:
    source: str
    relation: str
    target: str


class StateDatabase:
    """Read-only access to the local second-brain SQLite database."""

    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        if not self.db_path.exists():
            raise FileNotFoundError(f"state database not found: {self.db_path}")

    def _connect(self) -> sqlite3.Connection:
        # URI mode keeps retrieval read-only so the agent cannot mutate state.db.
        uri = f"file:{self.db_path.resolve()}?mode=ro"
        conn = sqlite3.connect(uri, uri=True)
        conn.row_factory = sqlite3.Row
        return conn

    def tables(self) -> list[str]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
            ).fetchall()
        return [row["name"] for row in rows]

    def relationships_for(self, entity: str, limit: int = 50) -> list[Relationship]:
        """Return graph edges touching an entity.

        Expected schema:
            relationships(source_id TEXT, relationship TEXT, target_id TEXT)

        Matching is case-insensitive and supports partial names to make natural
        prompts such as 'trade manager' useful without an LLM-generated SQL query.
        """
        if "relationships" not in self.tables():
            return []

        pattern = f"%{entity}%"
        sql = """
            SELECT source_id, relationship, target_id
            FROM relationships
            WHERE lower(source_id) LIKE lower(?)
               OR lower(target_id) LIKE lower(?)
            LIMIT ?
        """
        with self._connect() as conn:
            rows = conn.execute(sql, (pattern, pattern, limit)).fetchall()

        return [
            Relationship(
                source=str(row["source_id"]),
                relation=str(row["relationship"]),
                target=str(row["target_id"]),
            )
            for row in rows
        ]

    def find_nodes(self, terms: Iterable[str], limit: int = 30) -> list[str]:
        """Find node ids/names when a conventional nodes table is present.

        Supported columns are intentionally conservative: id and name. If the
        table is absent, relationship traversal still works.
        """
        if "nodes" not in self.tables():
            return []

        with self._connect() as conn:
            columns = {
                row["name"]
                for row in conn.execute("PRAGMA table_info(nodes)").fetchall()
            }
            searchable = [c for c in ("id", "name") if c in columns]
            if not searchable:
                return []

            found: list[str] = []
            for term in terms:
                conditions = " OR ".join(
                    f"lower({column}) LIKE lower(?)" for column in searchable
                )
                params = [f"%{term}%"] * len(searchable)
                rows = conn.execute(
                    f"SELECT * FROM nodes WHERE {conditions} LIMIT ?",
                    (*params, limit),
                ).fetchall()
                for row in rows:
                    value = row["id"] if "id" in columns else row["name"]
                    if value is not None and str(value) not in found:
                        found.append(str(value))
                    if len(found) >= limit:
                        return found
            return found
