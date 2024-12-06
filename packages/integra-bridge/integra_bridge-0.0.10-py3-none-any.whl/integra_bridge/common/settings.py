from pathlib import Path

from pydantic import PositiveInt, StrictStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=Path(__file__).parent.parent.parent / ".env",
        env_file_encoding="utf-8",
        extra="allow",
    )
    DEFAULT_CONNECTOR_TIMEOUT: PositiveInt = 120
    API_PREFIX: StrictStr = "/api/integra"


SETTINGS = Settings()
