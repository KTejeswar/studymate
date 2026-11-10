"""
Application settings – loaded from .env via pydantic-settings.
Contains only API keys, Mongo credentials, and core defaults.
"""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # API Keys
    openai_api_key: str = ""
    gemini_api_key: str = ""
    groq_api_key: str = ""

    # MongoDB
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_db_name: str = "studymate"

    # App Defaults
    default_user_id: str = "demo"
    upload_max_size_mb: int = 100

    @property
    def upload_max_bytes(self) -> int:
        return self.upload_max_size_mb * 1024 * 1024


settings = Settings()
