"""OpenAI-compatible API implementation.

Works with Qwen (DashScope), GPT, DeepSeek, and any other
OpenAI Chat Completions-compatible API.
"""

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
    """Map openai SDK exceptions to domain exceptions."""
    status_code = exc.status_code
    error_code = ""
    if exc.body and isinstance(exc.body, dict):
        error_code = (exc.body.get("error") or {}).get("code", "")

    mapped = _ERROR_MAP.get((status_code, error_code))
    if mapped:
        return mapped(str(exc))

    if 400 <= status_code < 500:
        return LLMBadRequestError(str(exc))
    if status_code >= 500:
        return LLMTemporaryError(str(exc))

    return LLMError(str(exc))


def _build_client(api_key: str, base_url: str) -> OpenAI:
    """Build an OpenAI client."""
    if not api_key:
        raise LLMConfigurationError(
            "API key is not configured. Set DASHSCOPE_API_KEY in .env"
        )
    return OpenAI(api_key=api_key, base_url=base_url)


class OpenAICompatibleClient(BaseLLMClient):
    """OpenAI-compatible LLM client.

    Supports Qwen (DashScope), GPT, DeepSeek, and any other
    service implementing the OpenAI Chat Completions interface.
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
        """Lazily initialized async client."""
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
