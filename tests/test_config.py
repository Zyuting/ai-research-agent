"""Configuration 模块测试。"""

from research_agent.config import Settings


def test_settings_defaults():
    """验证默认配置值。"""
    s = Settings()
    assert s.llm_model == "qwen-plus"
    assert s.search_engine == "duckduckgo"
    assert "dashscope" in s.llm_base_url
