from dataclasses import dataclass, field
from datetime import date
import re
from typing import List

from app.common.interface.entity import Entity



@dataclass
class JobSummary(Entity):
	job: str
	url: str 
	website: str
	# imported_on: date
	processed: bool = False
	
	 	

@dataclass 
class JobDetailled:
	job: str
	company: str
	city: str
	url: str 
	website: str
	contenu: str