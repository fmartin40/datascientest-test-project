from datetime import date
from pydantic import BaseModel

class Job(BaseModel):
    url: str 
    source: str


class JobSummary(BaseModel):
    url: str
    libelle: str| None = None
    source: str | None = None
    entreprise: str | None = None
    ville: str | None = None
    type_contrat: int | None = None
    
class JobDetail(BaseModel):
    url: str
    source: str
    job_id: str
    date_creation: date | None = date.today()
    libelle: str
    entreprise: str
    ville: str
    type_contrat: int
    mode_travail: int
    duree_travail: int
    competence: list[int] | None = None

