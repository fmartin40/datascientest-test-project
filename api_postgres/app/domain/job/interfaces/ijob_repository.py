from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.job.entities.jobs import Job
from pydantic import BaseModel

class IJobRepository(ABC):
    @abstractmethod
    def add(self, job: Job) -> None:
        raise NotImplementedError

    @abstractmethod
    def list(
    self,
    competence: Optional[str] = None,
    langue: Optional[str] = None,
    formation: Optional[str] = None,
    entreprise: Optional[str] = None,
    type_contrat: Optional[str] = None,
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
    def list_formations(self) -> List[BaseModel]:
        raise NotImplementedError

    @abstractmethod
    def list_langues(self) -> List[BaseModel]:
        raise NotImplementedError

    @abstractmethod
    def list_entreprises(self) -> List[BaseModel]:
        raise NotImplementedError

    @abstractmethod
    def list_salaires(self) -> List[BaseModel]:
        raise NotImplementedError 