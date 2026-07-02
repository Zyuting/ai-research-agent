"""LLM 客户端工厂函数。

调用方通过 get_llm() 获取实例，不感知具体实现类。
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
    """注册新的 LLM 提供商（扩展用）。"""
    _REGISTRY[name] = client_cls


def get_llm(provider: str | None = None) -> BaseLLMClient:
    """获取 LLM 客户端实例。

    Args:
        provider: 提供商名称，默认从配置读取 LLM_PROVIDER（当前仅支持 "openai"）。

    通义千问、GPT、DeepSeek 等均走 OpenAI Compatible API，
    只需修改 .env 中的 LLM_BASE_URL 和 LLM_MODEL 即可切换。
    """
    provider = provider or settings.llm_provider
    client_cls = _REGISTRY.get(provider)
    if client_cls is None:
        raise LLMConfigurationError(f"不支持的 LLM 提供商：{provider}")

    return client_cls(
        api_key=settings.dashscope_api_key,
        base_url=settings.llm_base_url,
        model=settings.llm_model,
    )
