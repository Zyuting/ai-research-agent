"""Planner node — generates search keywords from the user's topic."""

from __future__ import annotations

from research_agent.llm import get_llm
from research_agent.prompts import load_prompt
from research_agent.state import ResearchState


def planner_node(state: ResearchState) -> dict:
    """Generate 3-5 search queries from the research topic."""
    prompt = load_prompt("planner.txt", topic=state["topic"])
    llm = get_llm()
    resp = llm.invoke(prompt)

    queries = [
        line.strip().strip("-").strip()
        for line in resp.content.strip().split("\n")
        if line.strip()
    ]

    return {"search_queries": queries[:5]}
