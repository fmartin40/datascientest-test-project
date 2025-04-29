from typing import Dict, List
import json
import redis.asyncio as redis
from app.core.config import settings
from app.workers.common.entities.jobs import JobDetail
from app.workers.common.interfaces.iloader import ILoader

# ----------------------------------------------------
#               Fake db dans un json 
#  ----------------------------------------------------

class RedisDetail(ILoader):
    def __init__(self):
        try:
            self.redis = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
        except Exception as ce:
            raise Exception("Erreur de connection a Redis :", ce)
       
    async def insert(self, key: str, job:JobDetail|Dict):
        try:
            if isinstance(job, JobDetail):
                await self.redis.set(key, job.model_dump_json()) # type: ignore
            else:
                await self.redis.set(key, json.dumps(job), ex=300) # type: ignore  # noqa: F821
        except Exception as e:
            raise Exception(f"Erreur lors de l'insertion dans Redis: {e}")
     
    async def insert_many(self, jobs: List[JobDetail], table:str):
        raise NotImplementedError

    async def update(self, job_id: int):
        raise NotImplementedError