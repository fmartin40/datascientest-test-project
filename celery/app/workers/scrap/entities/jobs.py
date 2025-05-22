
from typing import List
from pydantic import BaseModel

class Job(BaseModel):
	url: str 
	website: str


class JobSummary(Job):
	url: str 
	website: str


class JobDetailInfos(BaseModel):
	technologies: list[str] | None = None
	contract_types: list[str] | None = None
	embeddings: list[float] | None = None

class JobDetail(Job):
	job_id: str
	title: str
	company: str
	city: str
	postal_code: int
	contract_type:str|List[str]
	description: str
	infos: JobDetailInfos | None = None
