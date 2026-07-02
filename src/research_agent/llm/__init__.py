"""LLM layer — unified interface for OpenAI-compatible APIs.

Provides BaseLLMClient, LLMResponse, and a get_llm() factory.
"""

from research_agent.llm.base import BaseLLMClient, LLMResponse
from research_agent.llm.factory import get_llm

__all__ = [
    "BaseLLMClient",
    "LLMResponse",
    "get_llm",
]
