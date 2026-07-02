"""LLM 抽象基类与统一返回值定义。"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class LLMResponse:
    """统一的 LLM 调用返回值。"""
    content: str
    model: str
    usage: dict[str, int] = field(default_factory=dict)


class BaseLLMClient(ABC):
    """LLM 客户端抽象基类。

    所有 LLM 实现（通义千问、GPT、DeepSeek 等）继承此类，
    调用方通过工厂函数 get_llm() 获取实例，不感知具体实现。
    """

    @abstractmethod
    def invoke(self, message: str, **kwargs: Any) -> LLMResponse:
        """同步调用。"""
        ...

    @abstractmethod
    async def ainvoke(self, message: str, **kwargs: Any) -> LLMResponse:
        """异步调用。"""
        ...
