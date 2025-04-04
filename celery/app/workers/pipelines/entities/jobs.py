
from typing import List
from pydantic import BaseModel

class Job(BaseModel):
	url: str 
	website: str

	model_config = {
        "extra": "ignore"  # ignore les clés inattendues
    }

class JobSummary(Job):
	pass


class JobDetailInfos(BaseModel):
	pass

	model_config = {
        "extra": "ignore"  # ignore les clés inattendues
    }

class JobDetail(Job):
	job_id: str
	title: str
	company: str
	city: str
	postal_code: int
	contract_type:str|List[str]
	description: str
	infos: JobDetailInfos | None = None
