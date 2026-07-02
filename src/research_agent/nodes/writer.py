"""Report Writer Node - 根据摘要生成最终 Markdown 报告。"""

from __future__ import annotations

from research_agent.llm import get_llm
from research_agent.prompts import load_prompt
from research_agent.state import ResearchState


def writer_node(state: ResearchState) -> dict:
    """根据摘要生成 Markdown 报告。"""
    summary = state.get("summary", "无内容。")
    prompt = load_prompt("report_writer.txt", topic=state["topic"], summary=summary)

    llm = get_llm()
    resp = llm.invoke(prompt)

    return {"report": resp.content}
