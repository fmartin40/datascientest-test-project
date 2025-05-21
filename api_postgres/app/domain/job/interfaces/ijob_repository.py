from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.job.entities.jobs import Job
from pydantic import BaseModel

class IJobRepository(ABC):
    @abstractmethod
    def add(self, job: Job) -> None:
        pass

    @abstractmethod
    def list(self, competence: Optional[str] = None) -> List[Job]:
        pass

    @abstractmethod
    def get(self, job_id: str) -> Optional[Job]:
        pass

    @abstractmethod
    def delete(self, job_id: str) -> bool:
        pass

    @abstractmethod
    def list_competences(self) -> List[BaseModel]:
        pass

    @abstractmethod
    def list_formations(self) -> List[BaseModel]:
        pass

    @abstractmethod
    def list_langues(self) -> List[BaseModel]:
        pass

    @abstractmethod
    def list_entreprises(self) -> List[BaseModel]:
        pass

    @abstractmethod
    def list_salaires(self) -> List[BaseModel]:
        pass 