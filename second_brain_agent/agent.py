from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .context import ContextBuilder, ContextBundle
from .inference import GitHubModelsClient, InferenceResult


SYSTEM_INSTRUCTION = """You are an engineering assistant using a local second-brain context bundle.
Use the retrieved context when it is relevant. Distinguish facts present in the context from inference.
If the context is insufficient, say what is missing rather than inventing repository facts.
Do not claim to have queried files or databases beyond the supplied context bundle.
"""


@dataclass(frozen=True)
class AgentResult:
    answer: str
    context: ContextBundle
    inference: InferenceResult


class SecondBrainAgent:
    """Retrieves local knowledge first, then calls the configured model endpoint."""

    def __init__(
        self,
        *,
        db_path: Path,
        markdown_root: Path,
        model_client: GitHubModelsClient,
    ):
        self.context_builder = ContextBuilder(
            db_path=db_path,
            markdown_root=markdown_root,
        )
        self.model_client = model_client

    def ask(self, prompt: str, *, note_limit: int = 8) -> AgentResult:
        prompt = prompt.strip()
        if not prompt:
            raise ValueError("prompt cannot be empty")

        context = self.context_builder.build(prompt, note_limit=note_limit)
        context_text = context.as_markdown()

        user_message = (
            "Answer the user's engineering question using the local second-brain context below.\n\n"
            "--- BEGIN LOCAL CONTEXT ---\n"
            f"{context_text}\n"
            "--- END LOCAL CONTEXT ---\n\n"
            "User question:\n"
            f"{prompt}"
        )

        inference = self.model_client.complete(
            [
                {"role": "system", "content": SYSTEM_INSTRUCTION},
                {"role": "user", "content": user_message},
            ]
        )

        return AgentResult(
            answer=inference.text,
            context=context,
            inference=inference,
        )
