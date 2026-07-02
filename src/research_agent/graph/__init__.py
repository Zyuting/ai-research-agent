"""LangGraph workflow assembly.

Flow:
  START → planner → search → reader → summarizer → writer → END

Each node is an independent function. Data flows through ResearchState only.
"""

from langgraph.graph import END, StateGraph

from research_agent.nodes import (
    planner_node,
    reader_node,
    search_node,
    summarizer_node,
    writer_node,
)
from research_agent.state import ResearchState


def build_graph() -> StateGraph:
    """Build the AI Research Agent LangGraph.

    Returns:
        A compiled StateGraph — call .invoke() to run.
    """
    workflow = StateGraph(ResearchState)

    # Register nodes
    workflow.add_node("planner", planner_node)
    workflow.add_node("search", search_node)
    workflow.add_node("reader", reader_node)
    workflow.add_node("summarizer", summarizer_node)
    workflow.add_node("writer", writer_node)

    # Wire edges
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "search")
    workflow.add_edge("search", "reader")
    workflow.add_edge("reader", "summarizer")
    workflow.add_edge("summarizer", "writer")
    workflow.add_edge("writer", END)

    return workflow.compile()


# Singleton — reuse the compiled graph across invocations
graph = build_graph()
