"""Search 和 Web Reader 的统一数据模型。"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SearchResult:
    """搜索单条结果。"""
    title: str
    url: str
    snippet: str


@dataclass
class WebPage:
    """网页读取结果。"""
    url: str
    title: str
    content: str
    html: str = field(default="", repr=False)
