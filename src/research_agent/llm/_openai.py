"""OpenAI Compatible API 实现（通义千问、GPT、DeepSeek 等均可通过此接口调用）。"""

from __future__ import annotations

from typing import Any

import openai
from openai import OpenAI, APIStatusError, APITimeoutError, RateLimitError

from research_agent.llm.base import BaseLLMClient, LLMResponse
from research_agent.llm.errors import (
    LLMAuthenticationError,
    LLMBadRequestError,
    LLMConfigurationError,
    LLMRateLimitError,
    LLMTemporaryError,
)


_ERROR_MAP: dict[tuple[int, str], type] = {
    (401, "authentication_error"): LLMAuthenticationError,
    (403, "permission_error"): LLMAuthenticationError,
    (404, "not_found"): LLMBadRequestError,
    (400, "bad_request"): LLMBadRequestError,
    (400, "context_length_exceeded"): LLMBadRequestError,
    (429, "rate_limit_error"): LLMRateLimitError,
    (500, "server_error"): LLMTemporaryError,
    (503, "service_unavailable"): LLMTemporaryError,
}


def _map_error(exc: APIStatusError) -> LLMError:
    """将 openai SDK 异常映射为业务异常。"""
    status_code = exc.status_code
    error_code = ""
    if exc.body and isinstance(exc.body, dict):
        error_code = (exc.body.get("error") or {}).get("code", "")

    mapped = _ERROR_MAP.get((status_code, error_code))
    if mapped:
        return mapped(str(exc))

    # 兜底：4xx → 请求错误，5xx → 临时错误
    if 400 <= status_code < 500:
        return LLMBadRequestError(str(exc))
    if status_code >= 500:
        return LLMTemporaryError(str(exc))

    return LLMError(str(exc))


def _build_client(api_key: str, base_url: str) -> OpenAI:
    """构建 OpenAI 客户端。"""
    if not api_key:
        raise LLMConfigurationError(
            "API Key 未配置，请设置 DASHSCOPE_API_KEY 环境变量"
        )
    return OpenAI(api_key=api_key, base_url=base_url)


class OpenAICompatibleClient(BaseLLMClient):
    """OpenAI Compatible API LLM 客户端。

    兼容通义千问（DashScope）、GPT、DeepSeek 等所有
    实现了 OpenAI Chat Completions 接口的模型服务。
    """

    def __init__(
        self,
        *,
        api_key: str,
        base_url: str,
        model: str,
    ) -> None:
        self._client = _build_client(api_key, base_url)
        self._model = model

    @property
    def model(self) -> str:
        return self._model

    def invoke(self, message: str, **kwargs: Any) -> LLMResponse:
        try:
            raw = self._client.chat.completions.create(
                model=self._model,
                messages=[{"role": "user", "content": message}],
                **kwargs,
            )
        except RateLimitError as e:
            raise LLMRateLimitError(str(e)) from e
        except APITimeoutError as e:
            raise LLMTemporaryError(str(e)) from e
        except APIStatusError as e:
            raise _map_error(e) from e

        return self._build_response(raw)

    async def ainvoke(self, message: str, **kwargs: Any) -> LLMResponse:
        try:
            raw = await self._async_client.chat.completions.create(
                model=self._model,
                messages=[{"role": "user", "content": message}],
                **kwargs,
            )
        except RateLimitError as e:
            raise LLMRateLimitError(str(e)) from e
        except APITimeoutError as e:
            raise LLMTemporaryError(str(e)) from e
        except APIStatusError as e:
            raise _map_error(e) from e

        return self._build_response(raw)

    # ---- private ----

    @property
    def _async_client(self):
        """延迟初始化的 async client。"""
        try:
            return self.__async_client
        except AttributeError:
            self.__async_client = openai.AsyncOpenAI(
                api_key=self._client.api_key,
                base_url=str(self._client.base_url),
            )
            return self.__async_client

    @staticmethod
    def _build_response(raw: Any) -> LLMResponse:
        choice = raw.choices[0]
        return LLMResponse(
            content=choice.message.content or "",
            model=raw.model,
            usage=dict(raw.usage or {}),
        )
