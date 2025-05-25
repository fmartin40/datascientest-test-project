from typing import List

from app.workers.entities.jobs import JobDetail
from app.workers.interfaces.iloader import ILoader

# ----------------------------------------------------
#               Fake db dans un json 
#  ----------------------------------------------------

class PostgresLoader(ILoader):
    async def insert(self, job:JobDetail):
        raise NotImplementedError
    
    async def insert_many(self, jobs: List[JobDetail]):
        raise NotImplementedError

    async def update(self, job_id: int):
        raise NotImplementedError