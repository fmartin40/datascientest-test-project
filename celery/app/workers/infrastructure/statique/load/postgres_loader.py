from typing import List, Dict
import logging

from app.workers.entities.jobs import JobDetail
from app.workers.interfaces.iloader import ILoader
from app.workers.infrastructure.statique.load.fetch import Fetch, RequestConfig
from app.core.config import settings

logger = logging.getLogger(__name__)


class PostgresLoader(ILoader):
    def __init__(self):
        self.api = Fetch()
        self.query = RequestConfig(
            method="POST",
            url=settings.ENDPOINT_POSTGRES_JOBCREATE,
            payload=None,
            params=None,
            headers={"Content-Type": "application/json"},
        )

    async def insert(self, job: JobDetail):
        """
        Stocke un document JSON dans PostgreSQL.
        :param job_data: Dictionnaire contenant les données de l'offre d'emploi.
        :param doc_id: (Optionnel) ID du document dans Elasticsearch.
        :return: Résultat de l'insertion.
        """
        payload: Dict = {
            "job_id": job.job_id,
            "libelle": job.libelle,
            "date_creation": job.date_creation,
            "source": job.source,
            "url": job.url,
            "entreprise": job.entreprise,
            "ville": job.ville,
            "type_contrat_id": job.type_contrat,
            "mode_travail_id": job.mode_travail,
            "duree_travail_id": job.duree_travail,
            "competence_ids": job.competence,
        }
        self.query.payload = payload
        logger.info(f"Insertion du job dans PostgreSQL: {self.query.model_dump()}")
        response = await self.api.fetch(self.query)
        return response

    async def insert_many(self, jobs: List[JobDetail], table: str):
        raise NotImplementedError

    async def update(self, job_id: int):
        raise NotImplementedError
