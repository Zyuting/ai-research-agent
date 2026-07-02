"""LLM abstract base class and unified response type."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class LLMResponse:
    """Unified LLM call response."""
    content: str
    model: str
    usage: dict[str, int] = field(default_factory=dict)


class BaseLLMClient(ABC):
    """Abstract base class for LLM clients.

    All LLM implementations (Qwen, GPT, DeepSeek, etc.) inherit from this.
    Callers obtain instances via get_llm() factory — never instantiate directly.
    """

    @abstractmethod
    def invoke(self, message: str, **kwargs: Any) -> LLMResponse:
        """Synchronous call."""
        ...

    @abstractmethod
    async def ainvoke(self, message: str, **kwargs: Any) -> LLMResponse:
        """Asynchronous call."""
        ...
