from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    """Application settings."""

    APP_NAME: str = "web-browser-mcp-server"
    APP_VERSION: str = "0.1.2"
    LOG_LEVEL: str = "info"
    USER_AGENT: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )
    REQUEST_TIMEOUT: int = 30
    MAX_RETRIES: int = 3

    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")
