from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

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
    date_creation: Optional[datetime] = None

    source_id: Optional[int]
    entreprise_id: Optional[int]
    ville_id: Optional[int]
    type_contrat_id: Optional[int]
    experience_id: Optional[int]
    duree_travail_id: Optional[int]
    mode_travail_id: Optional[int]
    salaire_id: Optional[int]

    formation_ids: Optional[List[int]] = None
    langue_ids: Optional[List[int]] = None
    competence_ids: Optional[List[int]] = None

