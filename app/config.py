from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    database_url: str = "sqlite+aiosqlite:///./neutral_news.db"
    log_level: str = "INFO"

    pipeline_interval_minutes: int = 30
    cluster_similarity_threshold: float = 0.35
    max_articles_per_fetch: int = 50

    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    ollama_url: str = ""
    ollama_model: str = "llama3"

    use_gdelt: bool = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
