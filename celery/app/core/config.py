import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIR = Path(__file__).parent.parent.parent
DOTENV = os.path.join(ROOT_DIR, '.env')


class Settings(BaseSettings):
	model_config = SettingsConfigDict(env_file=DOTENV, extra="ignore")
	
	CONFIG_FOLDER: str = "app/infrastructure/pipelines/pipeline_settings/files"
	
	ENVIRONMENT: str = "local"  #  (local ou prod)

	REDIS_HOST_LOCAL: str = "localhost"
	REDIS_HOST_PROD: str 
	REDIS_PORT: int 
	REDIS_DB: int 

	# Base de données (choix automatique selon l'environnement)
	POSTGRES_USER: str
	POSTGRES_PASSWORD: str
	POSTGRES_DB: str
	POSTGRES_HOST_LOCAL: str 
	POSTGRES_HOST_PROD: str 

	# Elasticsearch (choix automatique selon l'environnement)
	ELASTIC_HOST_LOCAL: str = "http://127.0.0.1:9200"
	ELASTIC_HOST_PROD: str 
	ELASTIC_INDEX: str = "jobs"

	CELERY_RESULT_BACKEND: str = "rpc://"

	RABBITMQ_URL_LOCAL: str = "localhost"
	RABBITMQ_URL_PROD: str 
	RABBITMQ_DEFAULT_USER: str
	RABBITMQ_DEFAULT_PASS: str

	API_SCRAP_PORT: int

	@property
	def SCRAP_API_TEST_RESULT_URL(self):
		return f"http://api_scrap:{self.API_SCRAP_PORT}/profile/test/scraping-result"
	
	@property
	def POSTGRES_HOST(self):
		return self.POSTGRES_HOST_PROD if self.ENVIRONMENT == "prod" else self.POSTGRES_HOST_LOCAL

	@property
	def ELASTIC_HOST(self):
		return self.ELASTIC_HOST_PROD if self.ENVIRONMENT == "prod" else self.ELASTIC_HOST_LOCAL

	@property
	def RABBITMQ_URL(self):
		return self.RABBITMQ_URL_PROD if self.ENVIRONMENT == "prod" else self.RABBITMQ_URL_LOCAL

	@property
	def REDIS_HOST(self):
		return self.REDIS_HOST_PROD if self.ENVIRONMENT == "prod" else self.REDIS_HOST_LOCAL



settings = Settings()  # type: ignore
