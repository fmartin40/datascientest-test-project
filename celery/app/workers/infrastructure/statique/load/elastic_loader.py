from typing import List

from app.workers.entities.jobs import JobDetail
from app.workers.interfaces.iloader import ILoader
from app.workers.infrastructure.statique.load.fetch import Fetch, RequestConfig
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class ElasticLoader(ILoader):
    def __init__(self):
        self.api = Fetch()
        self.query = RequestConfig(
            method="POST",
            url=settings.ENDPOINT_ELASTIC_JOBCREATE,
            payload=None,
            params=None,
            headers={"Content-Type": "application/json"},
        )

    async def insert(self, job: JobDetail):
        """
        Stocke un document JSON dans Elasticsearch.
        :param job_data: Dictionnaire contenant les données de l'offre d'emploi.
        :param doc_id: (Optionnel) ID du document dans Elasticsearch.
        :return: Résultat de l'insertion.
        """
        self.query.payload = job.model_dump(
            include={"job_id", "libelle", "date_creation", "description", "url"}
        )
        logger.info(f"Insertion du job dans Elasticsearch: {self.query.model_dump()}")
        response = await self.api.fetch(self.query)
        return response

    async def insert_many(self, jobs: List[JobDetail]):
        raise NotImplementedError

    async def update(self, job_id: int):
        raise NotImplementedError
