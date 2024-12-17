from enum import Enum
from app.scrap.infra.scrap.selectorlib.scraper_indeed import ScraperIndeedService
from app.scrap.infra.scrap.selectorlib.scraper_jungle import ScraperJungleService
from app.scrap.infra.scrap.selectorlib.scraper_muse import ScraperMuseService
from app.scrap.interfaces.iscrape_service import IJobScraper

class Website(Enum):
    MUSE:str = "muse"
    JUNGLE: str = "jungle"
    INDEED:str = "indeed"

def get_scraper(website: Website)->IJobScraper:
    match website:
        case Website.MUSE:
            return ScraperMuseService()
        case Website.JUNGLE:
            return ScraperJungleService()
        case Website.INDEED:
            return ScraperIndeedService()

        case _:
            raise ValueError(f"Service non supporté pour le site : {website}")
