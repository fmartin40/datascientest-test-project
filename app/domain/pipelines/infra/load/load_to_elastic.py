

from typing import List
from elasticsearch import Elasticsearch
import elasticsearch.exceptions as EsException


from app.core.config import settings
from app.domain.pipelines.entities.jobs import Job
from app.domain.common.errors.errors import RepositoryError
from app.domain.pipelines.interfaces.ijob_load import IJobLoadToRepository

# ----------------------------------------------------
#               Fake db dans un json 
#  ----------------------------------------------------

class JobsInElastic(IJobLoadToRepository):
    def __init__(self):
        try:
            self.es = Elasticsearch(hosts=[settings.ELASTIC_HOST])
            self.index = settings.ELASTIC_INDEX
        except ConnectionError as ce:
            raise RepositoryError("Erreur de connection a Elasticsearch :", ce)
        self._create_index()
        print('initialisé')

    def _create_index(self):
        """
        Crée l'index s'il n'existe pas.
        """
        if not self.es.indices.exists(index=self.index):
            settings = {
                "settings": {
                    "number_of_shards": 1,
                    "number_of_replicas": 1
                },
                "mappings": {
                    "properties": {
                        "title": {"type": "text"},
                        "company": {"type": "text"},
                        "city": {"type": "text"},
                        "postal_code": {"type": "keyword"},
                        "type": {"type": "keyword"},
                        "description": {"type": "text"},
                    }
                }
            }
            self.es.indices.create(index=self.index, body=settings)

    async def insert(self, job:Job):
        """
        Stocke un document JSON dans Elasticsearch.
        :param job_data: Dictionnaire contenant les données de l'offre d'emploi.
        :param doc_id: (Optionnel) ID du document dans Elasticsearch.
        :return: Résultat de l'insertion.
        """
        try:
            response = self.es.index(index=self.index, body=vars(job))
            return response
        except Exception as e:
            raise RepositoryError(f"Erreur lors de l'insertion dans Elasticsearch: {e}")
    
    async def insert_many(self, jobs: List[Job], table:str):
        raise NotImplementedError

    async def update(self, job_id: int):
        raise NotImplementedError