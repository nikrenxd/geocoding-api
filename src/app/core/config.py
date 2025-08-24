from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENV: str = Literal["DEV", "PROD", "TEST"]
    DB_URL: str
    TEST_DB_URL: str
    API_KEY: str
    model_config = SettingsConfigDict(env_file=".env")


def create_config() -> Settings:
    return Settings()
