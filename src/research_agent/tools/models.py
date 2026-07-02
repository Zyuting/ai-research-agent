"""Data models for search and web reader tools."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SearchResult:
    """A single search result entry."""
    title: str
    url: str
    snippet: str


@dataclass
class WebPage:
    """Fetched web page content."""
    url: str
    title: str
    content: str
    html: str = field(default="", repr=False)
