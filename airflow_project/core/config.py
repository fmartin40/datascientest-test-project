import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIR = Path(__file__).parent.parent.parent
DOTENV = os.path.join(ROOT_DIR, ".env")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=DOTENV, extra="ignore")

    API_SCRAP_PORT: int
    API_ELASTIC_PORT: int
    API_POST_PORT: int

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int

    CELERY_RESULT_BACKEND: str = "rpc://"

    RABBITMQ_URL: str
    RABBITMQ_DEFAULT_USER: str
    RABBITMQ_DEFAULT_PASS: str

    API_SCRAP_PORT: int


settings = Settings()  # type: ignore
