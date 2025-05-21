from typing import List, Optional, Any
from pydantic import BaseModel
from datetime import datetime

class Entreprise(BaseModel):
    id: int
    libelle: Optional[str]

class Salaire(BaseModel):
    id: int
    libelle: Optional[str]

class Formation(BaseModel):
    id: int
    libelle: Optional[str]

class Langue(BaseModel):
    id: int
    libelle: Optional[str]

class Competence(BaseModel):
    id: int
    libelle: Optional[str]

class Source(BaseModel):
    id: int
    libelle: Optional[str]

class ModeTravail(BaseModel):
    id: int
    libelle: Optional[str]

class Experience(BaseModel):
    id: int
    libelle: Optional[str]

class DureeTravail(BaseModel):
    id: int
    libelle: Optional[str]

class Job(BaseModel):
    # id: int | None = None
    job_id: str
    source: Optional[Source]
    libelle: Optional[str] = None
    date_creation: Optional[datetime] = None
    entreprise: Optional[Entreprise] = None
    type_contrat: Optional[str] = None
    experience: Optional[Experience] = None
    duree_travail: Optional[DureeTravail] = None
    mode_travail: Optional[ModeTravail] = None
    salaire: Optional[Salaire] = None
    formations: Optional[List[Formation]] = None
    langues: Optional[List[Langue]] = None
    competences: Optional[List[Competence]] = None
