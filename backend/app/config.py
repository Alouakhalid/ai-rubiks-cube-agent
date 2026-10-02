from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    PROJECT_NAME: str = "AI Rubik's Cube Agent"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "qwen-2.5-32b"
    COHERE_API_KEY: str = ""
    COHERE_EMBED_MODEL: str = "embed-english-v3.0"
    COHERE_RERANK_MODEL: str = "rerank-v3.5"
    MAX_AGENT_TURNS: int = 10
    CORS_ORIGINS: List[str] = ["*"]


settings = Settings()
