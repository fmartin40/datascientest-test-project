from abc import ABC, abstractmethod
from typing import Dict

class IMappings(ABC):
    @abstractmethod
    async def list_type_contrat(self) -> Dict[str, int]:
        raise NotImplementedError

    @abstractmethod
    async def list_mode_travail(self) -> Dict[str, int]:
        raise NotImplementedError
    
    @abstractmethod
    async def list_duree_travail(self) -> Dict[str, int]:
        raise NotImplementedError
    
    @abstractmethod
    async def list_competence(self) -> Dict[str, int]:
        raise NotImplementedError

