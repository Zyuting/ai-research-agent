"""Summarizer Node - 综合多个网页内容生成摘要。"""

from __future__ import annotations

from research_agent.llm import get_llm
from research_agent.prompts import load_prompt
from research_agent.state import ResearchState


def _format_pages(state: ResearchState) -> str:
    """将网页内容格式化为 LLM 可读的文本块。"""
    pages = state.get("web_pages", [])
    blocks: list[str] = []
    for i, page in enumerate(pages, 1):
        blocks.append(f"[来源 {i}] 标题: {page.title}\nURL: {page.url}\n内容:\n{page.content[:2000]}")
    return "\n\n---\n\n".join(blocks)


def summarizer_node(state: ResearchState) -> dict:
    """综合多个来源生成摘要。"""
    pages_text = _format_pages(state)
    if not pages_text.strip():
        return {"summary": "未能获取到有效的网页内容。"}

    prompt = load_prompt("summarizer.txt", topic=state["topic"], pages_text=pages_text)
    llm = get_llm()
    resp = llm.invoke(prompt)

    return {"summary": resp.content}
