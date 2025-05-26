from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class EntrepriseCreate(BaseModel):
    libelle: str

class VilleCreate(BaseModel):
    libelle: str

class CompetenceCreate(BaseModel):
    libelle: str

class SourceCreate(BaseModel):
    libelle: str

class ModeTravailCreate(BaseModel):
    libelle: str

class DureeTravailCreate(BaseModel):
    libelle: str

class TypeContratCreate(BaseModel):
    libelle: str

class JobCreate(BaseModel):
    job_id: str
    libelle: Optional[str] = None
    date_creation: Optional[date] = None
    source: str
    entreprise: str
    ville: str
    type_contrat_id: int
    duree_travail_id: int
    mode_travail_id: int
    competence_ids: Optional[List[int]] = None

