
from typing import List
from pydantic import BaseModel


class Job(BaseModel):
	job_id: str
	url: str 
	website: str
	title: str
	company: str
	city: str
	postal_code: int
	contract_type:str|List[str]
	description: str
