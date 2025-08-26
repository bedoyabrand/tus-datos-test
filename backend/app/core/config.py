from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    # DB
    DATABASE_URL: str = "postgresql+psycopg://postgres:postgres@db:5432/mis_eventos"

    # Auth
    JWT_SECRET: str = "devsecret"
    JWT_ALG: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 8

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:5173"]

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


settings = Settings()
