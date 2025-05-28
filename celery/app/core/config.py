import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIR = Path(__file__).parent.parent.parent
DOTENV = os.path.join(ROOT_DIR, ".env")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=DOTENV, extra="ignore")

    API_SCRAP_URL: str
    API_ELASTIC_URL: str
    API_POSTGRES_URL: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int

    CELERY_RESULT_BACKEND: str = "rpc://"

    RABBITMQ_URL: str
    RABBITMQ_DEFAULT_USER: str
    RABBITMQ_DEFAULT_PASS: str

    API_SCRAP_PORT: int

    @property
    def ENDPOINT_MAPPING(self) -> str:
        return f"{self.API_POSTGRES_URL}/mappings"

    @property
    def ENDPOINT_POSTGRES_JOBCREATE(self) -> str:
        return f"{self.API_POSTGRES_URL}/jobs/create"

    @property
    def ENDPOINT_ELASTIC_JOBCREATE(self) -> str:
        return f"{self.API_ELASTIC_URL}/jobs/create"


settings = Settings()  # type: ignore
