import re
from typing import Dict, List
from nodriver import *
from selectorlib import Extractor
from pathlib import Path

from app.scrap.entites.jobs import JobDetailled, JobSummary
from app.scrap.interfaces.iscrape_service import IJobScraper
from app.scrap.errors.errors import FetchApiException
from app.scrap.infra.scrap.selectorlib.fetch import FetchUrl


class ScraperIndeedService(FetchUrl, IJobScraper):
    def __init__(self):
        self.website_url: str = "https://fr.indeed.com"
        self.job_summaries_url: str = "/jobs"
        self.job_detailled_url: str = "/jobs"

    async def __build_url(self, query: str, cursor: str | None = None) -> Dict:
        query: str = re.sub(r"\s+", "+", query)
        params: str = f"?q={query}"
        if cursor:
            params += f"&start={cursor}"
        return f"{self.website_url}{self.job_summaries_url}{params}"

    async def __get_browser_content(self, url: str):
        browser = await start(
            headless=False,
            lang="fr-FR",  # this could set iso-language-code in navigator, not recommended to change
        )
        page = await browser.get(url)
        html = await page.get_content()
        await browser.wait(2)
        await page.close()
        return html

    def __scrape_page(self, html: str):
        try:
            # Appliquer les règles définies dans le fichier YAML
            current_file_path = Path(__file__).resolve()
            patterns_folder = current_file_path.parent / "patterns"
            pattern_file = patterns_folder / "rules_indeed.yaml"

            extractor = Extractor.from_yaml_file(pattern_file)
            data = extractor.extract(html)
            return data
        except Exception as e:
            print(f"Error: {e}")
            return None

    async def scrap_jobs_summaries(
        self, query: str, limit: int = 100, cursor: str | None = None
    ) -> List[JobSummary]:
        try:
            url: str = await self.__build_url(query, cursor)
            html: str = await self.__get_browser_content(url)
            jobs: List[Dict] = self.__scrape_page(html)
            return [
                JobSummary.create(**job, website="indeed", processed=False)
                for job in jobs.get("jobs")
            ]
        except FetchApiException as exc:
            raise exc
        except Exception:
            raise

    async def scrap_job_content(
        self, url: str, website: str, *args, **kwargs
    ) -> List[JobDetailled]:
        raise NotImplementedError
