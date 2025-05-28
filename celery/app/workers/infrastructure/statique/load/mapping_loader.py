import json
import redis
from typing import Dict
from app.workers.infrastructure.statique.load.fetch import Fetch, RequestConfig
from app.core.config import settings
from app.workers.interfaces.ikeyword_loader import IKeywordLoader
import logging

# ----------------------------------------------------
#               Fake db dans un json
#  ----------------------------------------------------
logger = logging.getLogger(__name__)


class MappingsFromPostgres(IKeywordLoader):
    def __init__(self):
        try:
            self.redis = redis.Redis(
                host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
            )
            self.api = Fetch()
            self.request = RequestConfig(
                method="GET",
                url="",
                payload=None,
                params=None,
                headers={"Content-Type": "application/json"},
            )
        except Exception as ce:
            raise Exception("Erreur de connection a Redis :", ce)

    async def load_competences(self):
        return await self._load_keywords("competences")

    async def load_duree_travail(self):
        return await self._load_keywords("duree-travail")

    async def load_mode_travail(self):
        return await self._load_keywords("mode-travail")

    async def load_type_contrat(self):
        return await self._load_keywords("types-contrat")

    async def load_ville(self):
        return await self._load_keywords("villes")

    async def _load_keywords(self, cache_key: str) -> Dict[str, str]:
        self.request.url = f"{settings.ENDPOINT_MAPPING}/{cache_key}"
        data: Dict = self.redis.get(cache_key)  # type: ignore
        if data:
            if isinstance(data, bytes):
                data: str = data.decode("utf-8")  # type: ignore
            dico: Dict[str, str] = json.loads(data)  # type: ignore
            return dico

        response: Dict[str, str] = await self.api.fetch(self.request)  # type: ignore
        keywords: Dict[str, str] = response
        self.redis.set(cache_key, json.dumps(keywords, ensure_ascii=False), ex=3600)
        logger.info("keywords mises en cache")
        return keywords
