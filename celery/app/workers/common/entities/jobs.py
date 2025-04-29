
from typing import Dict, List
from pydantic import BaseModel

class Job(BaseModel):
	url: str 
	website: str


class JobSummary(Job):
	url: str 
	website: str


class JobDetail(Job):
	job_id: str
	title: str
	company: str
	city: str
	postal_code: int
	contract_type:str|List[str]
	description: str
	infos: Dict | None = None

class JobDetailInfos(BaseModel):
	pass