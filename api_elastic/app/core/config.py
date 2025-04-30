from functools import lru_cache
import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIR = Path(__file__).parent.parent.parent
DOTENV = os.path.join(ROOT_DIR, '.env')


class Settings(BaseSettings):
	model_config = SettingsConfigDict(env_file=DOTENV, extra = "allow")
	
	# cette variable est utilisée pour déterminer si l'environnement est local ou en production
	# elle est mise a jour dans le docker-compose.yml
	ENVIRONMENT:str ="local"  # "local" ou "prod"

	INDEX_JOBS: str = "jobs"
	ELASTIC_USERNAME: str
	ELASTIC_PASSWORD: str

	# ELASTIC_HOST_LOCAL: str = "http://localhost"
	# ELASTIC_HOST_PROD: str  # Nouvelle variable pour l'environnement de production
	ELASTIC_HOST: str = "http://elasticsearch"

	ELASTIC_INDEX: str
	ES_PORT: int

	# @property
	# def ELASTIC_HOST(self):
	# 	return self.ELASTIC_HOST_PROD if self.ENVIRONMENT == "prod" else self.ELASTIC_HOST_LOCAL

@lru_cache
def get_settings():
	return Settings()  # type: ignore

settings = get_settings()  # type: ignore
