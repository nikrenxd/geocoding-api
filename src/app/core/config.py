from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_URL: str
    API_KEY: str
    model_config = SettingsConfigDict(env_file=".env")


def create_config() -> Settings:
    return Settings()
