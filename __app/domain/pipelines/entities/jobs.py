from dataclasses import dataclass
from app.domain.common.interface.entity import Entity



@dataclass
class Job(Entity):
	job_id: str
	title: str
	url: str 

@dataclass
class JobSummary(Job):
	website: str
	processed: bool = False
		 	
@dataclass 
class JobDetail(Job):
	website: str
	company: str
	city: str
	postal_code: int
	contract_type:str
	description: str