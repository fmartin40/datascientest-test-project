from typing import List

from app.workers.entities.jobs import JobDetail
from app.workers.interfaces.iloader import ILoader

# ----------------------------------------------------
#               Fake db dans un json 
#  ----------------------------------------------------

class ElasticLoader(ILoader):
    async def insert(self, job:JobDetail):
        """
        Stocke un document JSON dans Elasticsearch.
        :param job_data: Dictionnaire contenant les données de l'offre d'emploi.
        :param doc_id: (Optionnel) ID du document dans Elasticsearch.
        :return: Résultat de l'insertion.
        """
        raise NotImplementedError
    
    async def insert_many(self, jobs: List[JobDetail]):
        raise NotImplementedError

    async def update(self, job_id: int):
        raise NotImplementedError