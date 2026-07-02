"""Application configuration via environment variables."""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    # LLM
    llm_provider: str = Field("openai", alias="LLM_PROVIDER")
    dashscope_api_key: str = Field("", alias="DASHSCOPE_API_KEY")
    llm_base_url: str = Field(
        "https://dashscope.aliyuncs.com/compatible-mode/v1",
        alias="LLM_BASE_URL",
    )
    llm_model: str = Field("qwen-plus", alias="LLM_MODEL")

    # Search
    search_engine: str = Field("duckduckgo", alias="SEARCH_ENGINE")


settings = Settings()
