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
    type_contrat: str | None = None
    
class JobDetail(BaseModel):
    url: str
    source: str
    job_id: str
    date_publication: str | None = date.today().strftime("%Y-%m-%d")
    libelle: str
    description: str
    entreprise: str | None = None
    ville: str | None = None
    type_contrat: str | None = None
    mode_travail: str | None = None
    duree_travail: str | None = None
    salaire: str | None = None
    formation: str | None = None
    # experience: str | None = None 
    # langue: list[str] | None = None
    competence: list[str] | None = None

