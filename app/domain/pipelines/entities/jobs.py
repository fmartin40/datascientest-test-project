from dataclasses import dataclass
from app.domain.common.interface.entity import Entity


@dataclass
class Job(Entity):
	pass


@dataclass
class JobSummary(Job):
	job: str
	url: str 
	website: str
	# imported_on: date
	processed: bool = False
		 	

@dataclass 
class JobDetail(Job):
	url: str 
	website: str
	title: str
	company: str
	city: str
	postal_code: int
	type:str
	description: str