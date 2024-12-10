from dataclasses import dataclass, field
import re
from typing import List


@dataclass
class JobSummary:
	company: str
	job_name: str
	url: str = field(init=False)
	processed: bool = False
	

@dataclass 
class JobMuse:
    company_size: str | None = None
    company_domain: List[str]
    contenu: str

    def __post_init__(self):
        if self.company_size:
            self.company_size = re.sub(r'Size\:\s*','',self.company_size)
        if self.company_domain:
            industries: str = re.sub(r'Industry:\s*','',self.company_domain)
            self.company_domain = industries.split(',')
