from datetime import date
from typing import List, Optional
from pydantic import BaseModel


class Job(BaseModel):
    job_id: str
    url: str | None = None
    libelle: str | None = None
    date_creation: Optional[date] = date.today()
    description: str
