"""LangGraph State 定义。

节点之间只通过 State 传递数据，不直接相互调用。

Flow: topic → search_queries → search_results → web_pages → summary → report
"""

from __future__ import annotations

from typing import TypedDict

from research_agent.tools.models import SearchResult, WebPage


class ResearchState(TypedDict):
    """研究助手全局状态。"""

    # Input
    topic: str

    # Planner -> Search
    search_queries: list[str]

    # Search -> Reader
    search_results: list[SearchResult]

    # Reader -> Summarizer
    web_pages: list[WebPage]

    # Summarizer -> Writer
    summary: str

    # Writer (final output)
    report: str

    # Non-blocking errors accumulated across nodes
    errors: list[str]
