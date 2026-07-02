"""Workflow 端到端测试。

用法：
    pytest tests/ -v
"""

from research_agent.graph import graph


def test_workflow_builds():
    """验证 Graph 编译成功。"""
    assert graph is not None
    assert hasattr(graph, "invoke")


def test_workflow_invoke():
    """验证完整研究流程可运行。"""
    result = graph.invoke({"topic": "Python async"})

    assert "topic" in result
    assert "search_queries" in result
    assert "search_results" in result
    assert "web_pages" in result
    assert "summary" in result
    assert "report" in result

    assert isinstance(result["report"], str)
    assert len(result["report"]) > 0
