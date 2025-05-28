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

    async def list(self) -> List[Job]:
        resp = await self.es.search(index=self.index, query={"match_all": {}})
        return [Job(**hit["_source"]) for hit in resp["hits"]["hits"]]

    async def get(self, job_id: str) -> Optional[Job]:
        try:
            resp = await self.es.get(index=self.index, id=job_id)
            return Job(**resp["_source"])
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du job {job_id} : {e}")
            raise
