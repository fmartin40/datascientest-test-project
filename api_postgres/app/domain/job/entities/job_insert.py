from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class EntrepriseCreate(BaseModel):
    libelle: str

class VilleCreate(BaseModel):
    libelle: str

class SalaireCreate(BaseModel):
    libelle: str

class FormationCreate(BaseModel):
    libelle: str

class LangueCreate(BaseModel):
    libelle: str

class CompetenceCreate(BaseModel):
    libelle: str

class SourceCreate(BaseModel):
    libelle: str

class ModeTravailCreate(BaseModel):
    libelle: str

class ExperienceCreate(BaseModel):
    libelle: str

class DureeTravailCreate(BaseModel):
    libelle: str

class TypeContratCreate(BaseModel):
    libelle: str

class JobCreate(BaseModel):
    job_id: str
    libelle: Optional[str] = None
    date_creation: Optional[date] = None

    source_id: int
    mode_travail_id: int
    entreprise: str
    ville: str
    type_contrat: str
    experience: str
    duree_travail: str
    salaire: Optional[int]

    formation: Optional[List[str]] = None
    langue: Optional[List[str]] = None
    competence: Optional[List[str]] = None

