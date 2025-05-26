from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.job.entities.jobs import Job
from pydantic import BaseModel

class IJobReader(ABC):
    @abstractmethod
    def add(self, job: Job) -> None:
        raise NotImplementedError

    @abstractmethod
    def list(
    self,
    limit: int,
    offset: int,
    competence: Optional[int] = None,
    entreprise: Optional[int] = None,
    ville: Optional[int] = None,
    type_contrat: Optional[int] = None,
    duree_travail: Optional[int] = None,
    mode_travail: Optional[int] = None,
    experience: Optional[int] = None,
    salaire: Optional[int] = None,
    source: Optional[int] = None,
    light: bool = True,
    ) -> list[Job]:
        raise NotImplementedError

    @abstractmethod
    def get(self, job_id: str) -> Optional[Job]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, job_id: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def list_competences(self) -> List[BaseModel]:
        raise NotImplementedError


    
    @abstractmethod
    def list_entreprises(self) -> List[BaseModel]:
        raise NotImplementedError


    @abstractmethod
    def list_type_contrat(self) -> List[BaseModel]:
        raise NotImplementedError

    @abstractmethod
    def list_duree_travail(self) -> List[BaseModel]:
        raise NotImplementedError

    @abstractmethod
    def list_mode_travail(self) -> List[BaseModel]:
        raise NotImplementedError


    @abstractmethod
    def list_source(self) -> List[BaseModel]:
        raise NotImplementedError
