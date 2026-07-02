"""LangGraph state definition.

Nodes communicate exclusively through State — no direct function calls.

Data flow: topic → search_queries → search_results → web_pages → summary → report
"""

from __future__ import annotations

from typing import TypedDict

from research_agent.tools.models import SearchResult, WebPage


class ResearchState(TypedDict):
    """Global state for the research agent."""

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
