from abc import ABC, abstractmethod
from app.domain.job.entities.jobs import Job
from pydantic import BaseModel


class IJobWriter(ABC):
    @abstractmethod
    async def add(self, job: Job) -> None:
        """Ajoute une offre d'emploi complète"""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, job_id: str) -> bool:
        """Supprime une offre d'emploi"""
        raise NotImplementedError

    @abstractmethod
    async def add_competence(self, competence: str) -> BaseModel:
        raise NotImplementedError

    @abstractmethod
    async def add_langue(self, langue: str) -> BaseModel:
        raise NotImplementedError

    @abstractmethod
    async def add_entreprise(self, entreprise: str) -> BaseModel:
        raise NotImplementedError

    @abstractmethod
    async def add_type_contrat(self, type_contrat: str) -> BaseModel:
        raise NotImplementedError

    @abstractmethod
    async def add_duree_travail(self, duree_travail: str) -> BaseModel:
        raise NotImplementedError

    @abstractmethod
    async def add_mode_travail(self, mode_travail: str) -> BaseModel:
        raise NotImplementedError

    @abstractmethod
    async def add_source(self, source: str) -> BaseModel:
        raise NotImplementedError
