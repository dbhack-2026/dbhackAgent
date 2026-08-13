from __future__ import annotations

import argparse
from pathlib import Path

from .context import ContextBuilder


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Retrieve local state.db relationships and Markdown context for a prompt."
    )
    p.add_argument("prompt", help="Natural-language engineering question")
    p.add_argument("--repo-root", default=".", help="Repository root (default: current directory)")
    p.add_argument("--db", default="state.db", help="Path to state.db, relative to repo root")
    p.add_argument(
        "--notes",
        default=".",
        help="Markdown root, relative to repo root (default: whole repo)",
    )
    p.add_argument("--note-limit", type=int, default=8)
    return p


def main() -> int:
    args = parser().parse_args()
    repo_root = Path(args.repo_root).resolve()
    db_path = (repo_root / args.db).resolve()
    notes_root = (repo_root / args.notes).resolve()

    builder = ContextBuilder(db_path=db_path, markdown_root=notes_root)
    bundle = builder.build(args.prompt, note_limit=args.note_limit)
    print(bundle.as_markdown())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
