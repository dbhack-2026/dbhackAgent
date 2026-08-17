from __future__ import annotations

import sqlite3
import tempfile
import unittest
from pathlib import Path

from second_brain_agent.context import ContextBuilder


class ContextBuilderTest(unittest.TestCase):
    def test_retrieves_relationships_and_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            db_path = root / "state.db"
            notes = root / "knowledge"
            notes.mkdir()

            conn = sqlite3.connect(db_path)
            conn.execute("CREATE TABLE nodes (id TEXT PRIMARY KEY, name TEXT)")
            conn.execute(
                "CREATE TABLE relationships (source_id TEXT, relationship TEXT, target_id TEXT)"
            )
            conn.executemany(
                "INSERT INTO nodes(id, name) VALUES (?, ?)",
                [
                    ("trade-manager", "Trade Manager"),
                    ("kafka", "Kafka"),
                    ("sql-server", "SQL Server"),
                ],
            )
            conn.executemany(
                "INSERT INTO relationships VALUES (?, ?, ?)",
                [
                    ("trade-manager", "USES", "kafka"),
                    ("trade-manager", "STORES_IN", "sql-server"),
                ],
            )
            conn.commit()
            conn.close()

            (notes / "trade-manager.md").write_text(
                "# Trade Manager\nConsumes trade events from Kafka.\n", encoding="utf-8"
            )
            (notes / "kafka.md").write_text(
                "# Kafka\nUsed for trade event transport.\n", encoding="utf-8"
            )

            bundle = ContextBuilder(db_path, notes).build(
                "How does the trade manager use Kafka?"
            )

            edges = {(e.source, e.relation, e.target) for e in bundle.relationships}
            self.assertIn(("trade-manager", "USES", "kafka"), edges)
            self.assertTrue(any(n.path.name == "trade-manager.md" for n in bundle.notes))
            rendered = bundle.as_markdown()
            self.assertIn("trade-manager --USES--> kafka", rendered)


if __name__ == "__main__":
    unittest.main()
