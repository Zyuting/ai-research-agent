"""Search tool — DuckDuckGo search with pluggable search engine architecture."""

from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
from typing import Any

from ddgs import DDGS

from research_agent.config import settings
from research_agent.tools.models import SearchResult


class BaseSearchClient(ABC):
    """Abstract base class for search engine clients."""

    @abstractmethod
    def search(self, query: str, max_results: int = 5) -> list[SearchResult]:
        ...

    @abstractmethod
    async def asearch(self, query: str, max_results: int = 5) -> list[SearchResult]:
        ...


class DuckDuckGoSearchClient(BaseSearchClient):
    """DuckDuckGo search via the ddgs library (no API key required)."""

    def search(self, query: str, max_results: int = 5) -> list[SearchResult]:
        try:
            with DDGS() as ddgs:
                raw: list[dict[str, Any]] = list(
                    ddgs.text(query, max_results=max_results)
                )
        except Exception as e:
            raise RuntimeError(f"DuckDuckGo search failed: {e}") from e

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
    """Register a new search engine (extensibility hook)."""
    _REGISTRY[name] = client_cls


def get_search_client(engine: str | None = None) -> BaseSearchClient:
    """Get a search client instance.

    Args:
        engine: Engine name. Defaults to SEARCH_ENGINE in .env.
    """
    engine = engine or settings.search_engine
    client_cls = _REGISTRY.get(engine)
    if client_cls is None:
        raise ValueError(f"Unsupported search engine: {engine}")

    return client_cls()
