from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: SecretStr
    jwt_secret_key: SecretStr

    auth_issuer: str = "https://auth.sugar.local"
    auth_audience: str = "https://api.sugar.local"
    jwt_algorithm: str = "RS256"

    jwks_url: str | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()
