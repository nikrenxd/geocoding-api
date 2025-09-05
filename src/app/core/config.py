from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENV: str = Literal["DEV", "PROD", "TEST"]
    EXTERNAL_API_URL: str
    EXTERNAL_COORD_API_URL: str
    DB_URL: str
    TEST_DB_URL: str
    API_KEY: str

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


def create_config() -> Settings:
    return Settings()
