"""Prompt loader — loads .txt templates and renders with variables."""

from __future__ import annotations

import pathlib

_PROMPTS_DIR = pathlib.Path(__file__).parent


def load_prompt(name: str, **kwargs: str) -> str:
    """Load a prompt template and fill in variables.

    Args:
        name: Template filename (e.g., planner.txt).
        **kwargs: Template variable values.

    Returns:
        Rendered prompt string.
    """
    path = _PROMPTS_DIR / name
    template = path.read_text(encoding="utf-8")
    return template.format(**kwargs)


def list_prompts() -> list[str]:
    """List all available prompt templates."""
    return sorted(p.name for p in _PROMPTS_DIR.glob("*.txt"))
