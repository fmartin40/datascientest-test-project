from typing import List, Dict, Optional

from app.workers.entities.jobs import JobDetail
from app.workers.interfaces.iloader import ILoader
from app.workers.infrastructure.statique.load.fetch import (
    Fetch,
    RequestConfig,
    HTTPStatusError,
)
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class ElasticLoader(ILoader):
    def __init__(self):
        self.api = Fetch()
        self.query = RequestConfig(
            method="POST",
            url="",
            payload={},
            params={},
            headers={"Content-Type": "application/json"},
        )

    async def insert(self, job: JobDetail) -> Optional[Dict]:
        """
        Stocke un document JSON dans Elasticsearch.

        :param job: Instance de JobDetail contenant les données de l'offre d'emploi.
        :return: Résultat de l'insertion ou None en cas d'erreur.
        """
        self.query.url = settings.ENDPOINT_ELASTIC_JOBCREATE
        self.query.payload = job.model_dump(
            include={"job_id", "libelle", "date_creation", "description", "url"}
        )
        logger.info(
            f"Requête d'insertion: {self.query.url} avec payload: {self.query.payload}"
        )
        logger.info(f"Insertion du job dans Elasticsearch: {self.query.model_dump()}")

        try:
            response = await self.api.fetch(self.query)

            if isinstance(response, dict) and response.get("status_code") == 201:
                logger.info(" Job inséré avec succès dans Elasticsearch")
                return response
            else:
                logger.error(
                    f" Erreur lors de l'insertion du job dans Elasticsearch: {response}"
                )
                return None

        except HTTPStatusError as e:
            logger.error(
                f" Erreur HTTP lors de l'insertion du job dans Elasticsearch: {e}"
            )
            return None
        except Exception as e:
            logger.error(
                f" Erreur inattendue lors de l'insertion du job dans Elasticsearch: {e}"
            )
            return None

    async def insert_many(self, jobs: List[JobDetail]):
        raise NotImplementedError

    async def update(self, job_id: int):
        raise NotImplementedError
