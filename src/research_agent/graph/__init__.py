"""LangGraph Workflow 组装。

Workflow 流程：
  START → planner → search → reader → summarizer → writer → END

每个节点都是独立的函数，通过 State 传递数据。
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
    """构建 AI Research Agent 的 LangGraph。

    Returns:
        编译好的 StateGraph（可直接调用 .invoke()）。
    """
    workflow = StateGraph(ResearchState)

    # 注册节点
    workflow.add_node("planner", planner_node)
    workflow.add_node("search", search_node)
    workflow.add_node("reader", reader_node)
    workflow.add_node("summarizer", summarizer_node)
    workflow.add_node("writer", writer_node)

    # 设置边
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "search")
    workflow.add_edge("search", "reader")
    workflow.add_edge("reader", "summarizer")
    workflow.add_edge("summarizer", "writer")
    workflow.add_edge("writer", END)

    return workflow.compile()


# 单例：全局共用同一个编译好的图
graph = build_graph()
