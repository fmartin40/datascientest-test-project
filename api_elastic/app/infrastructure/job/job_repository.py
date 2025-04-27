from typing import List, Optional
from elasticsearch import AsyncElasticsearch
from app.core.config import settings
from app.domain.job.entities.jobs import Job
from app.domain.job.interfaces.ijob_repository import IJobRepository

class JobRepositoryElastic(IJobRepository):
    def __init__(self, es: AsyncElasticsearch):
        self.es = es
        self.index = settings.INDEX_JOBS

    async def add(self, job: Job) -> None:
        await self.es.index(index=self.index, id=job.job_id, document=job.model_dump())

    async def list(self) -> List[Job]:
        resp = await self.es.search(index=self.index, query={"match_all": {}})
        return [Job(**hit["_source"]) for hit in resp["hits"]["hits"]]

    async def get(self, job_id: str) -> Optional[Job]:
        try:
            resp = await self.es.get(index=self.index, id=job_id)
            return Job(**resp["_source"])
        except Exception:
            return None

    async def delete(self, job_id: str) -> bool:
        try:
            await self.es.delete(index=self.index, id=job_id)
            return True
        except Exception:
            return False 