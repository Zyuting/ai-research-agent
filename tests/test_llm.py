"""LLM 模块单元测试。"""

from research_agent.llm import BaseLLMClient, LLMResponse
from research_agent.llm.errors import (
    LLMAuthenticationError,
    LLMBadRequestError,
    LLMConfigurationError,
    LLMError,
    LLMRateLimitError,
    LLMTemporaryError,
)


def test_llm_response_creation():
    """验证 LLMResponse dataclass。"""
    resp = LLMResponse(content="hello", model="qwen-plus", usage={"tokens": 10})
    assert resp.content == "hello"
    assert resp.model == "qwen-plus"
    assert resp.usage["tokens"] == 10


def test_error_hierarchy():
    """验证异常层次结构。"""
    assert issubclass(LLMAuthenticationError, LLMError)
    assert issubclass(LLMBadRequestError, LLMError)
    assert issubclass(LLMConfigurationError, LLMError)
    assert issubclass(LLMRateLimitError, LLMError)
    assert issubclass(LLMTemporaryError, LLMError)
