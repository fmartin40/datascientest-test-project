import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIR = Path(__file__).parent.parent
DOTENV = os.path.join(ROOT_DIR, '.env')


class Settings(BaseSettings):
	model_config = SettingsConfigDict(env_file=DOTENV, extra="ignore")
	
	CONFIG_FOLDER: str = "app/infrastructure/pipelines/pipeline_settings/files"
	# Détection de l'environnement (local ou docker)
	ENVIRONMENT: str = "local"  # Valeur par défaut

	# Base de données (choix automatique selon l'environnement)
	POSTGRES_USER: str
	POSTGRES_PASSWORD: str
	POSTGRES_DB: str
	POSTGRES_HOST_LOCAL: str 
	POSTGRES_HOST_DOCKER: str 

	# Elasticsearch (choix automatique selon l'environnement)
	ELASTIC_HOST_LOCAL: str = "http://127.0.0.1:9200"
	ELASTIC_HOST_DOCKER: str = "http://elasticsearch:9200"
	ELASTIC_INDEX: str = "jobs"

	CELERY_RESULT_BACKEND: str = "rpc://"

	RABBITMQ_URL_LOCAL: str = "localhost"
	RABBITMQ_URL_PROD: str 
	RABBITMQ_DEFAULT_USER: str
	RABBITMQ_DEFAULT_PASS: str

	FASTAPI_WEBHOOK_URL: str = "http://scrap_api:8000/profile/test/scraping-result"
	
	@property
	def POSTGRES_HOST(self):
		return self.POSTGRES_HOST_DOCKER if self.ENVIRONMENT == "prod" else self.POSTGRES_HOST_LOCAL

	@property
	def ELASTIC_HOST(self):
		return self.ELASTIC_HOST_DOCKER if self.ENVIRONMENT == "prod" else self.ELASTIC_HOST_LOCAL

	@property
	def RABBITMQ_URL(self):
		return self.RABBITMQ_URL_PROD if self.ENVIRONMENT == "prod" else self.RABBITMQ_URL_LOCAL


settings = Settings()  # type: ignore
