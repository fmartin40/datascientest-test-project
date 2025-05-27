from datetime import date
from pydantic import BaseModel


class Job(BaseModel):
    url: str
    source: str


class JobSummary(BaseModel):
    url: str
    libelle: str
    source: str
    entreprise: str
    ville: str
    type_contrat: int


class JobDetail(BaseModel):
    url: str
    source: str
    job_id: str
    date_creation: date | str
    description: str
    libelle: str
    entreprise: str
    ville: str
    type_contrat: int
    mode_travail: int
    duree_travail: int
    competence: list[int] | None = None
