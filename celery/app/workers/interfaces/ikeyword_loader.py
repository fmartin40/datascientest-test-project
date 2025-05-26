from abc import ABC, abstractmethod


class IKeywordLoader(ABC):
    
    @abstractmethod
    async def load_competences(self, *args, **kwargs):
        raise NotImplementedError
    
    @abstractmethod
    async def load_mode_travail(self, *args, **kwargs):
        raise NotImplementedError
    
    @abstractmethod
    async def load_type_contrat(self, *args, **kwargs):
        raise NotImplementedError
    
    @abstractmethod
    async def load_duree_travail(self, *args, **kwargs):
        raise NotImplementedError