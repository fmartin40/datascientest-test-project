from typing import List, Optional, Any
from pydantic import BaseModel
from datetime import datetime

class Entreprise(BaseModel):
    id: int
    libelle: Optional[str]

class Ville(BaseModel):
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

class TypeContrat(BaseModel):
    id: int
    libelle: Optional[str]

class Job(BaseModel):
    # id: int | None = None
    job_id: str
    source: Optional[Source]
    libelle: Optional[str] = None
    date_creation: Optional[datetime] = None
    entreprise: Optional[Entreprise] = None
    ville: Optional[Ville] = None
    type_contrat: Optional[TypeContrat] = None
    experience: Optional[Experience] = None
    duree_travail: Optional[DureeTravail] = None
    mode_travail: Optional[ModeTravail] = None
    salaire: Optional[Salaire] = None
    formations: Optional[List[Formation]] = None
    langues: Optional[List[Langue]] = None
    competences: Optional[List[Competence]] = None

class JobLight(BaseModel):
    # id: int | None = None
    job_id: str
    libelle: Optional[str] = None
    entreprise: Optional[Entreprise] = None
    ville: Optional[Ville] = None
    type_contrat: Optional[TypeContrat] = None
    source: Optional[Source] = None
