from dataclasses import dataclass, field
from datetime import date
import re
from typing import List
from xml.dom.minidom import Entity


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
	job: str
	company: str
	city: str
	url: str 
	website: str
	contenu: str