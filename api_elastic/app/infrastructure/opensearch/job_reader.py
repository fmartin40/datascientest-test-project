from typing import List, Optional
from opensearchpy import OpenSearch
from app.core.config import settings
from app.domain.job.entities.jobs import Job
from app.domain.job.interfaces.ijob_reader import IJobReader
import logging
import httpx

logger = logging.getLogger(__name__)


class JobReaderOpenSearch(IJobReader):
    def __init__(self, es: OpenSearch):
        self.es = es
        self.index = settings.OPENSEARCH_JOB_INDEX
        self.elastic_host = settings.OPENSEARCH_HOST
        self.elastic_user = settings.OPENSEARCH_USERNAME
        self.elastic_password = settings.OPENSEARCH_PASSWORD

    def list(self, offset: int = 0, limit: int = 10) -> List[Job] | None:
        try:
            resp = self.es.search(
                index=self.index,
                body={"query": {"match_all": {}}},
                from_=offset,
                size=limit,
            )
            if resp:
                return [Job(**hit["_source"]) for hit in resp["hits"]["hits"]]
            else:
                return None
        except Exception as e:
            logger.error(f"Erreur lors de la recherche des jobs : {e}")
            raise

    def list_by_ids(self, ids: List[str]) -> List[Job] | None:
        try:
            resp = self.es.search(
                index=self.index,
                body={"query": {"ids": {"values": ids}}},
            )
            if resp:
                return [Job(**hit["_source"]) for hit in resp["hits"]["hits"]]
            else:
                return None
        except Exception as e:
            logger.error(f"Erreur lors de la recherche des jobs : {e}")
            raise

    def get(self, job_id: str) -> Optional[Job]:
        try:
            resp = self.es.get(index=self.index, id=job_id)
            if resp:
                return Job(**resp["_source"])
            else:
                return None
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du job {job_id} : {e}")
            return None  # ou `raise` selon ta logique métier

    async def search_by_description(self, text: str) -> List[Job]:
        """
        Recherche textuelle dans la description des offres d'emploi.
        """
        pass
