

from typing import List
from elasticsearch import Elasticsearch
import elasticsearch.exceptions as EsException


from app.core.config import settings
from app.domain.pipelines.entities.jobs import Job
from app.domain.common.errors.errors import RepositoryError
from app.domain.reporting.interfaces.ijob_search import IJobSearch

# ----------------------------------------------------
#               Fake db dans un json 
#  ----------------------------------------------------

class SearchInElastic(IJobSearch):
    def __init__(self):
        try:
            self.es = Elasticsearch(hosts=[settings.ELASTIC_HOST])
            self.index = settings.ELASTIC_INDEX
        except ConnectionError as ce:
            raise RepositoryError("Erreur de connection a Elasticsearch :", ce)
        
    def search_jobs(self, title=None, city=None, contract_type=None,  *args, **kwargs):
        """
        Recherche des offres d'emploi selon les critères fournis.
        :param title: Titre du poste (ex: "Architecte Big Data").
        :param city: Ville (ex: "Paris").
        :param contract_type: Type de contrat (ex: "FULL_TIME").
        :return: Liste des résultats trouvés.
        """
        query = {"bool": {"must": []}}

        if title:
            query["bool"]["must"].append({"match": {"title": title}})
        if city:
            query["bool"]["must"].append({"match": {"city": city}})
        if contract_type:
            query["bool"]["must"].append({"match": {"type": contract_type}})

        search_body = {"query": query}

        try:
            response = self.es.search(index=self.index, body=search_body)
            return response["hits"]["hits"]  # Retourne les résultats
        except Exception as e:
            raise RepositoryError(f"Erreur de recherche : {e}")
    
    async def insert_many(self, jobs: List[Job], table:str):
        raise NotImplementedError

    async def update(self, job_id: int):
        raise NotImplementedError