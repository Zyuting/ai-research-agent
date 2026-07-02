"""LLM client factory.

Callers use get_llm() to obtain an instance. The concrete implementation
is determined by configuration — callers never instantiate clients directly.
"""

from __future__ import annotations

from research_agent.config import settings
from research_agent.llm._openai import OpenAICompatibleClient
from research_agent.llm.base import BaseLLMClient
from research_agent.llm.errors import LLMConfigurationError


_REGISTRY: dict[str, type[BaseLLMClient]] = {
    "openai": OpenAICompatibleClient,
}


def register_provider(name: str, client_cls: type[BaseLLMClient]) -> None:
    """Register a new LLM provider (extensibility hook)."""
    _REGISTRY[name] = client_cls


def get_llm(provider: str | None = None) -> BaseLLMClient:
    """Get an LLM client instance.

    Args:
        provider: Provider name. Defaults to LLM_PROVIDER from .env.

    Qwen, GPT, DeepSeek all use the OpenAI-compatible protocol.
    Switch models by changing LLM_BASE_URL and LLM_MODEL in .env.
    """
    provider = provider or settings.llm_provider
    client_cls = _REGISTRY.get(provider)
    if client_cls is None:
        raise LLMConfigurationError(f"Unsupported LLM provider: {provider}")

    return client_cls(
        api_key=settings.dashscope_api_key,
        base_url=settings.llm_base_url,
        model=settings.llm_model,
    )
