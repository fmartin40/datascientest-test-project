from opensearchpy import OpenSearch
from app.core.config import settings
from app.domain.job.entities.jobs import Job
from app.domain.job.interfaces.ijob_writer import IJobWriter
import logging

logger = logging.getLogger(__name__)


class JobWriterOpenSearch(IJobWriter):
    def __init__(self, es: OpenSearch):
        self.es = es
        self.index = settings.OPENSEARCH_JOB_INDEX

    def add(self, job: Job) -> None:
        try:
            if self.es.exists(index=self.index, id=job.job_id):
                logger.error(f"L'offre d'emploi {job.job_id} existe déjà")
            else:
                self.es.index(index=self.index, id=job.job_id, body=job.model_dump())
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout du job {job.job_id} : {e}")
            raise

    def update(self, job: Job) -> None:
        try:
            self.es.update(index=self.index, id=job.job_id, body=job.model_dump())
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour du job {job.job_id} : {e}")
            raise

    def delete(self, job_id: str) -> bool:
        try:
            self.es.delete(index=self.index, id=job_id)
            return True
        except Exception as e:
            logger.error(f"Erreur lors de la suppression du job {job_id} : {e}")
            raise
