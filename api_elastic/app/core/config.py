from functools import lru_cache
import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIR = Path(__file__).parent.parent.parent
DOTENV = os.path.join(ROOT_DIR, '.env')


class Settings(BaseSettings):
	model_config = SettingsConfigDict(env_file=DOTENV, extra = "allow")
	
	
	JOB_INDEX: str = "offre_emploi"
	ELASTIC_USERNAME: str
	ELASTIC_PASSWORD: str

	ELASTIC_HOST: str = "http://elasticsearch"
	ELASTIC_INDEX: str = "offre_emploi"
	ES_PORT: int

	
@lru_cache
def get_settings():
	return Settings()  # type: ignore

settings = get_settings()  # type: ignore
