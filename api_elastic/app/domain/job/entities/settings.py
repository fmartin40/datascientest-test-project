
from typing import Dict, List
from pydantic import BaseModel

class JobDetailInfos(BaseModel):
	technologies: list[str]
	embeddings: list[float]

class JobDetail(BaseModel):
	url: str 
	website: str
	job_id: str
	title: str
	company: str
	city: str
	postal_code: int
	contract_type:str|List[str]
	description: str
	infos: JobDetailInfos | None = None






    
    