from functools import lru_cache
import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIR = Path(__file__).parent.parent
DOTENV = os.path.join(ROOT_DIR, '.env')


class Settings(BaseSettings):
	model_config = SettingsConfigDict(env_file=DOTENV, extra="ignore")
	
	ENVIRONMENT:str # "local" ou "prod"

	INDEX_JOBS: str = "jobs"
	# Password for the 'elastic' user (at least 6 characters)
	ELASTICSEARCH_USERNAME: str
	ELASTICSEARCH_PASSWORD: str

	ELASTICSEARCH_HOST_LOCAL: str
	ELASTICSEARCH_HOST: str
	ELASTICSEARCH_INDEX: str
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
	def ELASTICSEARCH_HOST(self):
		return self.ELASTICSEARCH_HOST if self.ENVIRONMENT == "prod" else self.ELASTICSEARCH_HOST_LOCAL

@lru_cache
def get_settings():
	return Settings()  # type: ignore

settings = get_settings()  # type: ignore
print(settings.ELASTICSEARCH_HOST)