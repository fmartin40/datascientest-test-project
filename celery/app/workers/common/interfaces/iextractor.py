from abc import ABC, abstractmethod

class IExtractor(ABC):
    @abstractmethod
    async def extract(self, *args, **kwargs) -> str:
        raise NotImplementedError
    
    