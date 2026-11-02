from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    LLM_PROVIDER: Literal["OPENAI", "CLAUDE",
                          "GEMINI", "GROQ", "OPENROUTER"] = "OPENAI"

    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-3.5-turbo"

    CLAUDE_API_KEY: str = ""
    CLAUDE_MODEL: str = "claude-3-haiku-20240307"

    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-pro"

    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama3-70b-8192"

    OPENROUTER_API_KEY: str = ""
    OPENROUTER_MODEL: str = "openrouter/auto"

    EMBEDDING_PROVIDER: Literal["OPENAI",
                                "HUGGINGFACE", "OPENROUTER"] = "OPENROUTER"
    OPENROUTER_EMBEDDING_MODEL: str = "openai/text-embedding-3-small"

    class Config:
        env_file = ".env"


settings = Settings()
