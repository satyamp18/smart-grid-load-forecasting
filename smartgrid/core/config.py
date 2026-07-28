from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/smartgrid"

    FRONTEND_URL: str = "http://localhost:5173"

    REDIS_URL: str | None = None

    SECRET_KEY: str | None = None

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    SKIP_DB_INIT: bool = False

    model_config = SettingsConfigDict(
        env_file=(".env.production", ".env.development", ".env"),
        extra="ignore",
    )


settings = Settings()