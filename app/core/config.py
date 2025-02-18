import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIR = Path(__file__).parent.parent.parent
DOTENV = os.path.join(ROOT_DIR, '.env')


class Settings(BaseSettings):
	model_config = SettingsConfigDict(env_file=DOTENV, extra="ignore")
	
	# Détection de l'environnement (local ou docker)
	ENVIRONMENT: str = "local"  # Valeur par défaut

	# Base de données (choix automatique selon l'environnement)
	POSTGRES_URL_LOCAL: str = "postgresql://root:root@localhost:5432/job_market"
	POSTGRES_URL_DOCKER: str = "postgresql://root:root@pgdatabase:5432/job_market"

	# Elasticsearch (choix automatique selon l'environnement)
	ELASTIC_HOST_LOCAL: str = "http://127.0.0.1:9200"
	ELASTIC_HOST_DOCKER: str = "http://elasticsearch:9200"
	ELASTIC_INDEX: str = "jobs"

	@property
	def DATABASE_URL(self):
		return self.POSTGRES_URL_DOCKER if self.ENVIRONMENT == "docker" else self.POSTGRES_URL_LOCAL

	@property
	def ELASTIC_HOST(self):
		return self.ELASTIC_HOST_DOCKER if self.ENVIRONMENT == "docker" else self.ELASTIC_HOST_LOCAL


settings = Settings()  # type: ignore
