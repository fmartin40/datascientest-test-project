from typing import List
import logging

from app.workers.entities.jobs import Job
from app.workers.interfaces.iloader import ILoader
from app.workers.infrastructure.statique.load.fetch import Fetch, RequestConfig
from app.core.config import settings

logger = logging.getLogger(__name__)

class PostgresLoader(ILoader):
    def __init__(self):
        self.api = Fetch()
        self.query = RequestConfig(
            method = "POST",
            url = f"http://api-postgres:{settings.API_POST_PORT}/jobs",
            payload = None,
            params = None,
            headers = {"Content-Type": "application/json"}
        )
    async def insert(self, job:Job):
        raise NotImplementedError
    
    async def insert_many(self, jobs: List[Job], table:str):
        raise NotImplementedError

    async def update(self, job_id: int):
        raise NotImplementedError