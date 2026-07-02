"""Reader Node - 遍历搜索结果，并发抓取网页正文。"""

from __future__ import annotations

import asyncio

from research_agent.state import ResearchState
from research_agent.tools import WebPage, get_web_reader


def _read_one(url: str) -> WebPage | None:
    """读取单个页面，失败返回 None。"""
    try:
        reader = get_web_reader()
        return reader.read(url)
    except Exception:
        return None


async def _read_all(urls: list[str]) -> list[WebPage]:
    """并发读取多个页面，过滤过短的内容。"""
    loop = asyncio.get_running_loop()
    tasks = [loop.run_in_executor(None, _read_one, u) for u in urls]
    results = await asyncio.gather(*tasks)
    return [r for r in results if r is not None and len(r.content) > 50]


def reader_node(state: ResearchState) -> dict:
    """并行抓取搜索结果中的网页。"""
    urls = [r.url for r in state.get("search_results", []) if r.url.startswith("http")]
    if not urls:
        return {"web_pages": [], "errors": state.get("errors", [])}

    pages = asyncio.run(_read_all(urls[:5]))

    errors = state.get("errors", []).copy()
    if not pages:
        errors.append("Reader: 所有页面均读取失败（被反爬拦截或网络不可达）")

    return {"web_pages": pages, "errors": errors}
