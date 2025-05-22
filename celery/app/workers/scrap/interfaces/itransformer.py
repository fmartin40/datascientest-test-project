from abc import ABC, abstractmethod

from app.workers.scrap.entities.jobs import JobDetail

class ITransformer(ABC):
    @abstractmethod
    async def transform(self, jobdetail: JobDetail, *args, **kwargs):
        raise NotImplementedError
    
    