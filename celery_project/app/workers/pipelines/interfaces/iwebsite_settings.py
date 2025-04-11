from abc import ABC, abstractmethod
from typing import Dict

from app.workers.pipelines.entities.settings import WebsiteSettings


class IWebsiteSettingsLoader(ABC):
    
    @abstractmethod
    def load_website_settings(self, website: str) -> WebsiteSettings:
        raise NotImplementedError
    
    @abstractmethod
    def create_website_settings(self, extract_config: Dict) -> WebsiteSettings:
        raise NotImplementedError
    