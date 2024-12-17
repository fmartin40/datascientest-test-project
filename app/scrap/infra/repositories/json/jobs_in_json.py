

import json
from pathlib import Path
from typing import List
from dataclasses import asdict
from app.scrap.entites.jobs import JobSummary
from app.scrap.interfaces.ijob_summary_repo import IJobSummaryRepository


class JobsInJsonRepo(IJobSummaryRepository):
    async def create(self, job:JobSummary):
        raise NotImplementedError
    
    async def create_many(self, jobs: List[JobSummary]):
        current_file_path = Path(__file__).resolve()
        db_folder = current_file_path.parent / "fake_db"
        jobs_in_file = db_folder / "jobs_summaries.json"
        jobs_as_dict = [[asdict(job) for job in jobs]]

        with open(jobs_in_file, 'w+') as file:
            json.dump(jobs_as_dict, file, indent=4, ensure_ascii=False)
    
    async def update(self, job_id: int):
        raise NotImplementedError