import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIR = Path(__file__).parent.parent.parent
DOTENV = os.path.join(ROOT_DIR, '.env')


class Settings(BaseSettings):
	model_config = SettingsConfigDict(env_file=DOTENV, extra="ignore")
	
	CONFIG_FOLDER: str = "app/infrastructure/pipelines/pipeline_settings/files"
	
	ENVIRONMENT: str = "local"  #  (local ou prod)

	REDIS_HOST: str 
	REDIS_HOST_PROD: str 
	REDIS_PORT: int 
	REDIS_DB: int 

	# Base de données (choix automatique selon l'environnement)
	POSTGRES_USER: str
	POSTGRES_PASSWORD: str
	POSTGRES_DB: str
	POSTGRES_HOST: str 
	POSTGRES_HOST_PROD: str 

	# Elasticsearch (choix automatique selon l'environnement)
	POSTGRES_HOST: str 
	ELASTIC_HOST_PROD: str 
	ELASTIC_INDEX: str = "jobs"

	CELERY_RESULT_BACKEND: str = "rpc://"

	RABBITMQ_URL: str 
	RABBITMQ_URL_PROD: str 
	RABBITMQ_DEFAULT_USER: str
	RABBITMQ_DEFAULT_PASS: str

	API_SCRAP_PORT: int

	@property
	def SCRAP_API_TEST_RESULT_URL(self):
		return f"http://api_scrap:{self.API_SCRAP_PORT}/profile/test/scraping-result"
	
	


settings = Settings()  # type: ignore
