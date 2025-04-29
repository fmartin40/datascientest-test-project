import json
from typing import Dict, List, Optional
import redis.asyncio as redis
from app.core.config import settings
from app.domain.profile.interfaces.ijob_repo import IJobRepo


class RedisLoader(IJobRepo):
    def __init__(self):
        try:
            self.redis = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB
            )
        except Exception as e:
            raise Exception(f"Erreur de connexion à Redis: {e}")

    async def get_job_detail(self, task_id: str) -> Optional[Dict]:
        try:
            data = await self.redis.get(task_id)
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération du job detail: {e}")

    async def get_job_summaries(self, task_id: str) -> Optional[List[Dict]]:
        try:
            data = await self.redis.get(task_id)
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération des job summaries: {e}") 