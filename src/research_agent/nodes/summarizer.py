"""Summarizer node — synthesizes a cross-source summary from web pages."""

from __future__ import annotations

from research_agent.llm import get_llm
from research_agent.prompts import load_prompt
from research_agent.state import ResearchState


def _format_pages(state: ResearchState) -> str:
    """Format web page content into LLM-readable text blocks."""
    pages = state.get("web_pages", [])
    blocks: list[str] = []
    for i, page in enumerate(pages, 1):
        blocks.append(
            f"[Source {i}] Title: {page.title}\nURL: {page.url}\nContent:\n{page.content[:2000]}"
        )
    return "\n\n---\n\n".join(blocks)


def summarizer_node(state: ResearchState) -> dict:
    """Synthesize a multi-source summary using LLM."""
    pages_text = _format_pages(state)
    if not pages_text.strip():
        return {"summary": "No valid web content was retrieved."}

    prompt = load_prompt("summarizer.txt", topic=state["topic"], pages_text=pages_text)
    llm = get_llm()
    resp = llm.invoke(prompt)

    return {"summary": resp.content}
