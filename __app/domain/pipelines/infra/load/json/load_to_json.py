

import json
from pathlib import Path
from typing import List
from dataclasses import asdict

from app.domain.pipelines.entities.jobs import Job, JobSummary
from app.domain.pipelines.interfaces.ijob_load import IJobLoadToRepository

# ----------------------------------------------------
#               Fake db dans un json 
#  ----------------------------------------------------

class JobsInJsonRepo(IJobLoadToRepository):
    def __init__(self):
        self.current_file_path = Path(__file__).resolve()
        self.db_folder = self.current_file_path.parent / "fake_db"

    async def insert(self, job:Job, table:str):
        jobs_in_file = self.db_folder / f"{table}.json"
        with open(jobs_in_file, 'w+') as file:
            json.dump(asdict(job), file, indent=4, ensure_ascii=False)
        return job
    
    async def insert_many(self, jobs: List[JobSummary], table:str):
        jobs_in_file = self.db_folder / f"{table}.json"
        jobs_as_dict = [[asdict(job) for job in jobs]]
        with open(jobs_in_file, 'w+') as file:
            json.dump(jobs_as_dict, file, indent=4, ensure_ascii=False)
        return jobs

    async def update(self, job_id: int):
        raise NotImplementedError