from __future__ import annotations

import argparse
from pathlib import Path

from .agent import SecondBrainAgent
from .context import ContextBuilder
from .inference import GitHubModelsClient, InferenceConfig, InferenceConfigError, InferenceError


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description=(
            "Retrieve local state.db/Markdown context and optionally send it to the "
            "configured GitHub Models compatible inference endpoint."
        )
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
    p.add_argument(
        "--context-only",
        action="store_true",
        help="Only print retrieved context; do not call the model endpoint",
    )
    p.add_argument(
        "--show-context",
        action="store_true",
        help="Print retrieved context before the model answer",
    )
    return p


def main() -> int:
    args = parser().parse_args()
    repo_root = Path(args.repo_root).resolve()
    db_path = (repo_root / args.db).resolve()
    notes_root = (repo_root / args.notes).resolve()

    if args.context_only:
        builder = ContextBuilder(db_path=db_path, markdown_root=notes_root)
        bundle = builder.build(args.prompt, note_limit=args.note_limit)
        print(bundle.as_markdown())
        return 0

    try:
        config = InferenceConfig.from_env()
        model_client = GitHubModelsClient(config)
        agent = SecondBrainAgent(
            db_path=db_path,
            markdown_root=notes_root,
            model_client=model_client,
        )
        result = agent.ask(args.prompt, note_limit=args.note_limit)
    except (InferenceConfigError, InferenceError, OSError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 2

    if args.show_context:
        print(result.context.as_markdown())
        print("\n--- MODEL ANSWER ---\n")

    print(result.answer)
    if result.inference.total_tokens is not None:
        print(f"\n[total_tokens={result.inference.total_tokens}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
