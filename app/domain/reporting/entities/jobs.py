from dataclasses import dataclass
from app.domain.common.interface.entity import Entity

	
@dataclass 
class JobDetail(Entity):
	job_id: str
	title: str
	url: str 
	website: str
	company: str
	city: str
	postal_code: int
	contract_type:str
	description: str