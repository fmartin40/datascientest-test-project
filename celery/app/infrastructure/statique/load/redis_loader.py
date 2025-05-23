from typing import Dict, List
import json
import redis
from app.core.config import settings
from app.workers.scrap.interfaces.iloader import ILoader
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
       
    def insert(self, key: str, job:Dict|List[Dict]):
        try:    
            if isinstance(job, list): 
                self._insert_summaries(key, job)
            else:
                self._insert_detail(key, job)
        except Exception as e:  
            logger.error(f"Erreur lors de l'insertion dans Redis: {e}")
            raise Exception(f"Erreur lors de l'insertion dans Redis: {e}")
    
    def _insert_detail(self, key: str, job:Dict):
        try:
            self.redis.set(key, json.dumps(job), ex=300) # type: ignore
        except Exception as e:
            logger.error(f"Erreur lors de l'insertion Detail dans Redis: {e}")
            raise Exception(f"Erreur lors de l'insertion Detail dans Redis: {e}")
        
    def _insert_summaries(self, key: str, job:List[Dict]):
        try:
            self.redis.set(key, json.dumps(job), ex=300) # type: ignore
        except Exception as e:
            logger.error(f"Erreur lors de l'insertion summaries dans Redis: {e}")
            raise Exception(f"Erreur lors de l'insertion summaries dans Redis: {e}")

    def insert_many(self, jobs: List[Dict], table:str):
        raise NotImplementedError

    def update(self, job_id: int):
        raise NotImplementedError