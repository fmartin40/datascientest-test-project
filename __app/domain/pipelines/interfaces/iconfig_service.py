from abc import ABC, abstractmethod
from typing import List

from app.domain.pipelines.entities.extractconfig import ExtractConfig

class IConfigService(ABC):
    
    @abstractmethod
    def get_website_config(self, website: str) -> ExtractConfig:
        raise NotImplementedError
    
    @abstractmethod
    def create_website_config(self, extract_config: ExtractConfig) -> ExtractConfig:
        raise NotImplementedError