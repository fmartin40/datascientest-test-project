from abc import ABC, abstractmethod

class IJobSearch(ABC):
    
    @abstractmethod
    def search_jobs(self, title=None, city=None, contract_type=None,  *args, **kwargs):
        raise NotImplementedError
    
    