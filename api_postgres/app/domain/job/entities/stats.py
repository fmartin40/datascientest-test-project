from pydantic import BaseModel
from datetime import date


class CompetenceByDateStats(BaseModel):
    date: date
    competence_id: int
    competence_libelle: str
    count: int
