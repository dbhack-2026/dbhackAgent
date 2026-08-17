"""Local second-brain retrieval and inference agent.

The package reads a local SQLite state database and Markdown files, builds a
compact context bundle, and can send that context to a configured GitHub
Models-compatible chat-completions endpoint.
"""

from .agent import AgentResult, SecondBrainAgent
from .context import ContextBuilder, ContextBundle
from .inference import (
    GitHubModelsClient,
    InferenceConfig,
    InferenceConfigError,
    InferenceError,
    InferenceResult,
)

__all__ = [
    "AgentResult",
    "ContextBuilder",
    "ContextBundle",
    "GitHubModelsClient",
    "InferenceConfig",
    "InferenceConfigError",
    "InferenceError",
    "InferenceResult",
    "SecondBrainAgent",
]
