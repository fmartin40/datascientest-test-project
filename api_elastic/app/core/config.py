from functools import lru_cache
import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIR = Path(__file__).parent.parent.parent
DOTENV = os.path.join(ROOT_DIR, ".env")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=DOTENV, extra="allow")

    ELASTIC_JOB_INDEX: str = "offre_emploi"
    ELASTIC_HOST: str
    ELASTIC_PORT: int
    ELASTIC_USERNAME: str
    ELASTIC_PASSWORD: str

    #
    # ELASTIC_INDEX: str = "offre_emploi"
    # ES_PORT: int

    OPENSEARCH_HOST: str
    OPENSEARCH_USERNAME: str
    OPENSEARCH_PASSWORD: str
    OPENSEARCH_PORT: int
    OPENSEARCH_JOB_INDEX: str = "offre_emploi"


@lru_cache
def get_settings():
    return Settings()  # type: ignore


settings = get_settings()  # type: ignore
