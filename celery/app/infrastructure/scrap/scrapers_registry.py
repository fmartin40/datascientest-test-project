from typing import Dict
import time
from app.workers.scrap.interfaces.iwebconfig import IWebsiteSettingsLoader
from app.infrastructure.scrap.scraper import Scraper
from app.workers.scrap.entities.settings import WebsiteSettings

class ScraperRegistry:
    def __init__(self, config_loader: IWebsiteSettingsLoader, ttl: int = 3600):
        self._loader = config_loader
        self._ttl = ttl
        self._last_reload = 0
        self._scrapers: Dict[str, Scraper] = {}


    def get_scraper(self, website: str) -> Scraper:
        self._refresh_scrapers_if_needed()
        return self._scrapers[website]

    def _refresh_scrapers_if_needed(self):
        now = time.time()
        if now - self._last_reload > self._ttl:
            self._load_all_scrapers()
            self._last_reload = now

    def _load_all_scrapers(self):
        self._scrapers.clear()
        website_names = self._loader.list_available_websites()
        for website in website_names:
            settings: WebsiteSettings = self._loader.load_website_settings(website)
            self._scrapers[website] = Scraper(settings)
