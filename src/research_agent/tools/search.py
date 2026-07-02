"""Search Tool 实现。

当前内置 DuckDuckGo（基于 ddgs 库），后续可扩展 Tavily、Google 等。
"""

from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
from typing import Any

from ddgs import DDGS

from research_agent.config import settings
from research_agent.tools.models import SearchResult


class BaseSearchClient(ABC):
    """搜索客户端抽象基类。"""

    @abstractmethod
    def search(self, query: str, max_results: int = 5) -> list[SearchResult]:
        ...

    @abstractmethod
    async def asearch(self, query: str, max_results: int = 5) -> list[SearchResult]:
        ...


class DuckDuckGoSearchClient(BaseSearchClient):
    """DuckDuckGo 搜索（基于 ddgs 库）。"""

    def search(self, query: str, max_results: int = 5) -> list[SearchResult]:
        try:
            with DDGS() as ddgs:
                raw: list[dict[str, Any]] = list(
                    ddgs.text(query, max_results=max_results)
                )
        except Exception as e:
            raise RuntimeError(f"DuckDuckGo 搜索失败: {e}") from e

        return [
            SearchResult(
                title=r.get("title", ""),
                url=r.get("href", ""),
                snippet=r.get("body", ""),
            )
            for r in raw
        ]

    async def asearch(self, query: str, max_results: int = 5) -> list[SearchResult]:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.search, query, max_results)


# ---- Registry & factory ----

_REGISTRY: dict[str, type[BaseSearchClient]] = {
    "duckduckgo": DuckDuckGoSearchClient,
}


def register_search_engine(name: str, client_cls: type[BaseSearchClient]) -> None:
    """注册新的搜索引擎（扩展用）。"""
    _REGISTRY[name] = client_cls


def get_search_client(engine: str | None = None) -> BaseSearchClient:
    """获取搜索客户端实例。

    Args:
        engine: 搜索引擎名称，默认读取 .env 中 SEARCH_ENGINE 配置。
    """
    engine = engine or settings.search_engine
    client_cls = _REGISTRY.get(engine)
    if client_cls is None:
        raise ValueError(f"不支持的搜索引擎: {engine}")

    return client_cls()
