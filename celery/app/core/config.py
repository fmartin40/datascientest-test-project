import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIR = Path(__file__).parent.parent.parent
DOTENV = os.path.join(ROOT_DIR, '.env')


class Settings(BaseSettings):
	model_config = SettingsConfigDict(env_file=DOTENV, extra="ignore")
	

	REDIS_HOST: str 
	REDIS_PORT: int 
	REDIS_DB: int 

	POSTGRES_USER: str
	POSTGRES_PASSWORD: str
	POSTGRES_DB: str
	POSTGRES_HOST: str 
	
	ELASTIC_HOST: str 
	ELASTIC_INDEX: str = "jobs"
	ES_PORT: int

	CELERY_RESULT_BACKEND: str = "rpc://"

	RABBITMQ_URL: str 
	RABBITMQ_DEFAULT_USER: str
	RABBITMQ_DEFAULT_PASS: str

	API_SCRAP_PORT: int

	

settings = Settings()  # type: ignore

