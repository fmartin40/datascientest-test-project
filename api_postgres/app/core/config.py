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

	POSTGRES_USER: str
	POSTGRES_PASSWORD: str
	POSTGRES_DB: str
	POSTGRES_PORT: int
	POSTGRES_HOST: str = "localhost"

	@property
	def POSTGRES_HOST_DB(self):
		if self.ENVIRONMENT == "prod":
			return self.POSTGRES_HOST
		return "localhost"

@lru_cache
def get_settings():
	return Settings()  # type: ignore

settings = get_settings()  # type: ignore

    