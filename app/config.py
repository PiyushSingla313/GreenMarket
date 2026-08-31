import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Defaults to a local SQLite file so the API runs out of the box with
    # zero setup. Point DATABASE_URL at Postgres for production, e.g.:
    # postgresql+psycopg2://user:password@host:5432/greenmarket
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./greenmarket.db")
    secret_key: str = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "10080"))
    cors_origins: str = os.getenv("CORS_ORIGINS", "*")

    class Config:
        env_file = ".env"


settings = Settings()
