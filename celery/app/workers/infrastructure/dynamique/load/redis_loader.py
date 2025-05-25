from typing import Dict, List
import json
import redis
from app.core.config import settings
from app.workers.interfaces.iloader import ILoader
import logging

# ----------------------------------------------------
#               Fake db dans un json 
#  ----------------------------------------------------
logger = logging.getLogger(__name__)

class RedisLoader(ILoader):
    def __init__(self):
        try:
            self.redis = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
        except Exception as ce:
            raise Exception("Erreur de connection a Redis :", ce)
       
    def insert(self, key: str, job:Dict|List[Dict], ttl:int=300):
        try:    
            if isinstance(job, list): 
                self._insert_summaries(key, job, ttl)
            else:
                self._insert_detail(key, job, ttl)
        except Exception as e:  
            logger.error(f"Erreur lors de l'insertion dans Redis: {e}")
            raise Exception(f"Erreur lors de l'insertion dans Redis: {e}")
    
    def insert_many(self, jobs: List[Dict], table:str):
        raise NotImplementedError

    def get_competences(self):
        try:
            return self.redis.get("competences")
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des compétences depuis Redis: {e}")
            raise Exception(f"Erreur lors de la récupération des compétences depuis Redis: {e}")

    def get_mode_travail(self):
        try:
            return self.redis.get("mode_travail")
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des modes de travail depuis Redis: {e}")
            raise Exception(f"Erreur lors de la récupération des modes de travail depuis Redis: {e}")
    
    def get_type_contrat(self):
        try:
            return self.redis.get("type_contrat")
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des types de contrats depuis Redis: {e}")
            raise Exception(f"Erreur lors de la récupération des types de contrats depuis Redis: {e}")
        
    def get_source(self):
        try:
            return self.redis.get("source")
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des sources depuis Redis: {e}")
            raise Exception(f"Erreur lors de la récupération des sources depuis Redis: {e}")
    
    
    def _insert_detail(self, key: str, job:Dict, ttl:int=300):
        try:
            self.redis.set(key, json.dumps(job), ex=ttl) # type: ignore
        except Exception as e:
            logger.error(f"Erreur lors de l'insertion Detail dans Redis: {e}")
            raise Exception(f"Erreur lors de l'insertion Detail dans Redis: {e}")
        
    def _insert_summaries(self, key: str, job:List[Dict], ttl:int=300):
        try:
            self.redis.set(key, json.dumps(job), ex=ttl) # type: ignore
        except Exception as e:
            logger.error(f"Erreur lors de l'insertion summaries dans Redis: {e}")
            raise Exception(f"Erreur lors de l'insertion summaries dans Redis: {e}")

    