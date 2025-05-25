from abc import ABC, abstractmethod
from typing import List

from app.workers.entities.settings import WebsiteSettings


class IWebsiteSettingsLoader(ABC):
    
    @abstractmethod
    def load_website_settings(self, website: str) -> WebsiteSettings:
        raise NotImplementedError
    
    @abstractmethod
    def list_available_websites(self) -> List[str]:
        raise NotImplementedError