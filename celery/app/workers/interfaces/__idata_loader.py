from abc import ABC, abstractmethod
from typing import List
from app.workers.entities.jobs import Job

class IDataLoader(ABC):
    
    @abstractmethod
    async def get_competences(self, *args, **kwargs):
        raise NotImplementedError
    
    @abstractmethod
    async def get_mode_travail(self, *args, **kwargs):
        raise NotImplementedError
    
    @abstractmethod
    async def get_type_contrat(self, *args, **kwargs):
        raise NotImplementedError
    
    @abstractmethod
    async def get_source(self, *args, **kwargs):
        raise NotImplementedError
    