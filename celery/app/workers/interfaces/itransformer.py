from abc import ABC, abstractmethod

class ITransformer(ABC):
    @abstractmethod
    async def transform(self, text: str, *args, **kwargs):
        raise NotImplementedError
    
    async def return_id(self, word: list[str] | str) -> list[int] | int | None:
        raise NotImplementedError
