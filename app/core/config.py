import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    API_DEFAULT_USER_NAME: str
    API_DEFAULT_USER_KEY: str

    REDIS_HOST: str
    REDIS_PORT: int

    RATE_LIMIT_REQUESTS: int

    class Config:
        env_file = ".env"


settings = Settings()
