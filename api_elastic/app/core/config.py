from functools import lru_cache
import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIR = Path(__file__).parent.parent
DOTENV = os.path.join(ROOT_DIR, '.env')


class Settings(BaseSettings):
	model_config = SettingsConfigDict(env_file=DOTENV, extra="ignore")
	
	ENVIRONMENT:str # "local" ou "prod"

	# Password for the 'elastic' user (at least 6 characters)
	ELASTICSEARCH_USERNAME: str
	ELASTIC_PASSWORD: str

	ELASTIC_HOST_LOCAL: str
	ELASTIC_HOST: str
	ELASTIC_INDEX: str
	ES_PORT: int

	# Elastic settings
	STACK_VERSION: str
	LICENSE: str
	ES_MEM_LIMIT: int
	KB_MEM_LIMIT: int
	LS_MEM_LIMIT: int
	CLUSTER_NAME: str

	# Kibana settings
	KIBANA_PASSWORD: str
	KIBANA_PORT: int

	# SAMPLE Predefined Key only to be used in POC environments
	ENCRYPTION_KEY: str

	
	@property
	def ELASTIC_HOST(self):
		return self.ELASTIC_HOST if self.ENVIRONMENT == "prod" else self.ELASTIC_HOST_LOCAL

@lru_cache
def get_settings():
	return Settings()  # type: ignore

settings = get_settings()  # type: ignore
