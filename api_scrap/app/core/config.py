import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIR = Path(__file__).parent.parent.parent
DOTENV = os.path.join(ROOT_DIR, '.env')


class Settings(BaseSettings):
	model_config = SettingsConfigDict(env_file=DOTENV, extra="allow")
	
	ENVIRONMENT: str = "local"  #  (local ou prod)

	REDIS_HOST_LOCAL: str = "localhost"
	REDIS_HOST_PROD: str 
	REDIS_PORT: int 
	REDIS_DB: int 

	CELERY_RESULT_BACKEND: str = "rpc://"

	RABBITMQ_URL_LOCAL: str = "localhost"
	RABBITMQ_URL_PROD: str 
	RABBITMQ_DEFAULT_USER: str
	RABBITMQ_DEFAULT_PASS: str

	@property
	def RABBITMQ_URL(self):
		return self.RABBITMQ_URL_PROD if self.ENVIRONMENT == "prod" else self.RABBITMQ_URL_LOCAL

	@property
	def REDIS_HOST(self):
		return self.REDIS_HOST_PROD if self.ENVIRONMENT == "prod" else self.REDIS_HOST_LOCAL
	
settings = Settings()  # type: ignore
