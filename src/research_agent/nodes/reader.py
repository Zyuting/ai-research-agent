"""Reader node — concurrently fetch pages from search results."""

from __future__ import annotations

import asyncio

from research_agent.state import ResearchState
from research_agent.tools import WebPage, get_web_reader


def _read_one(url: str) -> WebPage | None:
    """Fetch a single page, return None on failure."""
    try:
        reader = get_web_reader()
        return reader.read(url)
    except Exception:
        return None


async def _read_all(urls: list[str]) -> list[WebPage]:
    """Concurrently fetch multiple pages, discard too-short content."""
    loop = asyncio.get_running_loop()
    tasks = [loop.run_in_executor(None, _read_one, u) for u in urls]
    results = await asyncio.gather(*tasks)
    return [r for r in results if r is not None and len(r.content) > 50]


def reader_node(state: ResearchState) -> dict:
    """Fetch web pages from search results in parallel."""
    urls = [r.url for r in state.get("search_results", []) if r.url.startswith("http")]
    if not urls:
        return {"web_pages": [], "errors": state.get("errors", [])}

    pages = asyncio.run(_read_all(urls[:5]))

    errors = state.get("errors", []).copy()
    if not pages:
        errors.append("Reader: all pages failed to load (blocked or unreachable)")

    return {"web_pages": pages, "errors": errors}
