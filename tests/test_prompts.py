"""Prompts 模块测试。"""

from research_agent.prompts import list_prompts, load_prompt


def test_list_prompts():
    """验证能列出所有 prompt 文件。"""
    names = list_prompts()
    assert "planner.txt" in names
    assert "summarizer.txt" in names
    assert "report_writer.txt" in names


def test_load_planner_prompt():
    """验证 planner prompt 加载和模板渲染。"""
    text = load_prompt("planner.txt", topic="Python 异步编程")
    assert "Python 异步编程" in text
    assert "搜索关键词" in text


def test_load_summarizer_prompt():
    """验证 summarizer prompt 加载。"""
    text = load_prompt("summarizer.txt", topic="AI", pages_text="some content")
    assert "AI" in text
    assert "some content" in text


def test_load_report_writer_prompt():
    """验证 report_writer prompt 加载。"""
    text = load_prompt("report_writer.txt", topic="AI", summary="summary text")
    assert "AI" in text
    assert "summary text" in text
