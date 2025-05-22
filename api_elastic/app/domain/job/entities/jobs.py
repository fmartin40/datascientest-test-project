
from datetime import date
from typing import List, Optional
from pydantic import BaseModel


class Job(BaseModel):
    job_id: str
    libelle: Optional[str]
    date_creation: Optional[date] = date.today()
    description: str
