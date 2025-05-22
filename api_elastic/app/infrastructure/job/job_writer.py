from elasticsearch import AsyncElasticsearch
from app.core.config import settings
from app.domain.job.entities.jobs import Job
from app.domain.job.interfaces.ijob_writer import IJobWriter
import logging

logger = logging.getLogger(__name__)

class JobWriter(IJobWriter):
    def __init__(self, es: AsyncElasticsearch):
        self.es = es
        self.index = settings.JOB_INDEX

    async def add(self, job: Job) -> None:
        try:
            await self.es.index(index=self.index, id=job.job_id, document=job.model_dump())
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout du job {job.job_id} : {e}")
            raise

    async def update(self, job: Job) -> None:
        try:
            await self.es.update(index=self.index, id=job.job_id, doc=job.model_dump())
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour du job {job.job_id} : {e}")
            raise

    async def delete(self, job_id: str) -> bool:
        try:
            await self.es.delete(index=self.index, id=job_id)
            return True
        except Exception as e:
            logger.error(f"Erreur lors de la suppression du job {job_id} : {e}")
            raise
 
    


