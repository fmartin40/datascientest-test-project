from typing import Dict, List
import json
import redis.asyncio as redis
from app.core.config import settings
from app.workers.common.entities.jobs import JobSummary
from app.workers.common.interfaces.iloader import ILoader

# ----------------------------------------------------
#               Fake db dans un json 
#  ----------------------------------------------------

class RedisSummaries(ILoader):
    def __init__(self):
        try:
            self.redis = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
        except Exception as ce:
            raise Exception("Erreur de connection a Redis :", ce)
       
    async def insert(self, key:str, jobs:List[JobSummary]|Dict):
        try:
            if isinstance(jobs, List):
                jobs_json: List[str] = [job.model_dump_json() for job in jobs] # type: ignore
            else:
                jobs_json: Dict = jobs
            await self.redis.set(key, json.dumps(jobs_json), ex=300) # type: ignore
        except Exception as e:
            raise Exception(f"Erreur lors de l'insertion dans Redis: {e}")
    
    async def insert_many(self, jobs: List[JobSummary], table:str):
        raise NotImplementedError

    async def update(self, job_id: int):
        raise NotImplementedError