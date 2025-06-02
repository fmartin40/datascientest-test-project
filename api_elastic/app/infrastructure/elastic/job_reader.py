from typing import List, Optional
from elasticsearch import AsyncElasticsearch
from app.core.config import settings
from app.domain.job.entities.jobs import Job
from app.domain.job.interfaces.ijob_reader import IJobReader
import logging

logger = logging.getLogger(__name__)


class JobReaderElastic(IJobReader):
    def __init__(self, es: AsyncElasticsearch):
        self.es = es
        self.index = settings.ELASTIC_JOB_INDEX

    async def list(self, offset: int = 0, limit: int = 10) -> List[Job]:
        resp = await self.es.search(
            index=self.index,
            query={"match_all": {}},
            from_=offset,
            size=limit,
        )
        return [Job(**hit["_source"]) for hit in resp["hits"]["hits"]]

    async def get(self, job_id: str) -> Optional[Job]:
        try:
            resp = await self.es.get(index=self.index, id=job_id)
            return Job(**resp["_source"])
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du job {job_id} : {e}")
            raise

    async def list_by_ids(self, ids: List[str]) -> List[Job]:
        """
        Recherche des jobs par liste d'IDs.
        """
        try:
            resp = await self.es.search(
                index=self.index,
                query={"ids": {"values": ids}},
            )
            return [Job(**hit["_source"]) for hit in resp["hits"]["hits"]]
        except Exception as e:
            logger.error(f"Erreur lors de la recherche des jobs par IDs : {e}")
            raise

    async def search_by_description(
        self, text: str, offset: int = 0, limit: int = 10
    ) -> List[Job]:
        """
        Recherche textuelle dans la description des offres d'emploi.
        """
        try:
            resp = await self.es.search(
                index=self.index,
                query={"match_phrase": {"description": text}},
                from_=offset,
                size=limit,
            )
            return [Job(**hit["_source"]) for hit in resp["hits"]["hits"]]
        except Exception as e:
            logger.error(
                f"Erreur lors de la recherche textuelle dans la description : {e}"
            )
            raise
