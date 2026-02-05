from functools import lru_cache
import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIR = Path(__file__).parent.parent.parent
DOTENV = os.path.join(ROOT_DIR, ".env")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=DOTENV, extra="allow")

    API_SCRAP_URL: str
    API_ELASTIC_URL: str
    API_POSTGRES_URL: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int

    # LISTE_VILLE: str = "http://localhost:8003/ville"
    # LISTE_ENTREPRISE: str = "http://localhost:8003/entreprises"
    # LISTE_CONTRAT: str = "http://localhost:8003/types-contrat"
    # LISTE_DUREE: str = "http://localhost:8003/duree-travail"
    # LISTE_MODE: str = "http://localhost:8003/mode-travail"

    @property
    def LISTE_VILLE(self) -> str:
        return f"{self.API_POSTGRES_URL}/ville"

    @property
    def LISTE_ENTREPRISE(self) -> str:
        return f"{self.API_POSTGRES_URL}/entreprises"

    @property
    def LISTE_CONTRAT(self) -> str:
        return f"{self.API_POSTGRES_URL}/types-contrat"

    @property
    def LISTE_DUREE(self) -> str:
        return f"{self.API_POSTGRES_URL}/duree-travail"

    @property
    def LISTE_MODE(self) -> str:
        return f"{self.API_POSTGRES_URL}/mode-travail"

    @property
    def ENDPOINT_ELASTIC_JOB(self) -> str:
        return f"{self.API_POSTGRES_URL}/mappings"

    @property
    def ENDPOINT_POSTGRES_JOB(self) -> str:
        return f"{self.API_POSTGRES_URL}/jobs/create"

    @property
    def ENDPOINT_STAT_COMPETENCE_DAILY(self) -> str:
        return f"{self.API_POSTGRES_URL}/competences/daily"

    @property
    def ENDPOINT_STAT_COMPETENCE_SUM(self) -> str:
        return f"{self.API_POSTGRES_URL}/sum"


@lru_cache
def get_settings():
    return Settings()  # type: ignore


settings = get_settings()  # type: ignore
