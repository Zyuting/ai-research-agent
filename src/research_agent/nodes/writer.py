"""Writer node — generates the final Markdown report from summary."""

from __future__ import annotations

from research_agent.llm import get_llm
from research_agent.prompts import load_prompt
from research_agent.state import ResearchState


def writer_node(state: ResearchState) -> dict:
    """Generate a structured Markdown report from the summary."""
    summary = state.get("summary", "No content.")
    prompt = load_prompt("report_writer.txt", topic=state["topic"], summary=summary)

    llm = get_llm()
    resp = llm.invoke(prompt)

    return {"report": resp.content}
