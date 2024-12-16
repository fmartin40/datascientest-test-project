from dataclasses import dataclass, field
import re
from typing import List



@dataclass
class JobSummary:
	job: str
	url: str 
	website: str
	processed: bool = False
	 	

@dataclass 
class JobDetailled:
	job: str
	company: str
	city: str
	url: str 
	website: str
	contenu: str