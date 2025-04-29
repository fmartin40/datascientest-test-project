import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIR = Path(__file__).parent.parent.parent
DOTENV = os.path.join(ROOT_DIR, '.env')


class Settings(BaseSettings):
	model_config = SettingsConfigDict(env_file=DOTENV, extra="allow")
	
	CONFIG_FOLDER: str = "app/infrastructure/pipelines/pipeline_settings/files"
	
	# Détection de l'environnement (local ou docker)
	ENVIRONMENT: str = "local"  # Valeur par défaut

	CELERY_RESULT_BACKEND: str = "rpc://"

	RABBITMQ_URL_LOCAL: str = "localhost"
	RABBITMQ_URL_PROD: str 
	RABBITMQ_DEFAULT_USER: str
	RABBITMQ_DEFAULT_PASS: str

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
