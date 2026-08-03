from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "Vision-X API"
    project_name: str = "Vision-X"
    debug: bool = False
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.0-flash"

    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]


settings = Settings()
