from typing import List

from app.workers.pipelines.entities.jobs import Job
from app.workers.pipelines.interfaces.iloader import ILoader

# ----------------------------------------------------
#               Fake db dans un json 
#  ----------------------------------------------------

class PostgresLoader(ILoader):
    async def insert(self, job:Job):
        raise NotImplementedError
    
    async def insert_many(self, jobs: List[Job], table:str):
        raise NotImplementedError

    async def update(self, job_id: int):
        raise NotImplementedError