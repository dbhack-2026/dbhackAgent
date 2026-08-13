"""Local second-brain retrieval agent.

The package deliberately has no third-party runtime dependencies. It reads a
local SQLite state database and Markdown files, then builds a compact context
bundle that can be supplied to an LLM or IDE integration.
"""

from .context import ContextBuilder, ContextBundle

__all__ = ["ContextBuilder", "ContextBundle"]
