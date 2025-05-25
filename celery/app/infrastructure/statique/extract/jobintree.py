from typing import List, Dict
import urllib.parse
from glom import glom
import asyncio
import logging
import json
from html import unescape
from bs4 import BeautifulSoup
from app.infrastructure.dynamique.extract.fetchurl import FetchUrl
from app.workers.scrap.entities.jobs import JobDetail, JobSummary
from app.workers.scrap.interfaces.istatic_extractor import IStaticExtractor

logger = logging.getLogger(__name__)


class JobInTreeExtractor(IStaticExtractor):
    def __init__(self):
        self.fetch = FetchUrl()
        self.source: str = "jobintree"
        self.base_url: str = "https://www.jobintree.com"
        self.request_url: str = "/emploi/recherche.html?k={query}&l={location}"

    async def extract_summaries(
        self, query: str, location: str, loop: int
    ) -> List[JobSummary]:
        try:
            url = urllib.parse.urljoin(
                self.base_url, self.request_url.format(query=query, location=location)
            )
            content = await self._fetch(url=url)
            soup = BeautifulSoup(content, "html.parser")  # type: ignore
            summaries: List[JobSummary] = []

            job_offers = soup.select("article.card-job-offer")

            for job_offer in job_offers:
                a_tag = job_offer.select_one("h3.no-marg a")
                if a_tag is None:
                    continue

                summaries.append(
                    JobSummary(
                        libelle=a_tag.get_text(strip=True),  # type: ignore
                        url=urllib.parse.urljoin(self.base_url, a_tag.get("href")),  # type: ignore
                        source=self.source,
                        ville=job_offer.select("li.job-criteria-label span")[
                            1
                        ].get_text(strip=True),  # type: ignore
                        type_contrat=job_offer.select("li.job-criteria-label span")[
                            3
                        ].get_text(strip=True),  # type: ignore
                        entreprise=job_offer.select("li.job-criteria-label span")[
                            5
                        ].get_text(strip=True),  # type: ignore
                    )  # type: ignore
                )
            return summaries
        except Exception as exc:
            logger.error(f"Erreur dans extract_summaries: {exc}", exc_info=True)
            raise

    async def extract_details(self, job_summary: JobSummary) -> JobDetail | None:
        try:
            if not job_summary.url.startswith(self.base_url):
                job_summary.url = urllib.parse.urljoin(self.base_url, job_summary.url)

            content: str = await self.fetch.fetch(job_summary.url)

            jsons = BeautifulSoup(content, "html.parser").find_all(
                "script", {"type": "application/ld+json"}
            )  # type: ignore

            if not jsons:
                return None

            detail_required_json_keys: set = set(["description", "title"])
            selectors: dict = {
                "date_publication": "datePosted",
                "description": "description",
            }

            for js in jsons:
                json_to_parse: Dict = json.loads(js.string)  # type: ignore

                if detail_required_json_keys.issubset(json_to_parse.keys()):
                    parsed = glom(json_to_parse, selectors)  # type: ignore
                    logger.info(f"Parsed: {parsed}")

                    jobdetail = JobDetail(
                        job_id="1",
                        url=job_summary.url,
                        libelle=job_summary.libelle,  # type: ignore
                        ville=job_summary.ville,
                        type_contrat=job_summary.type_contrat,
                        entreprise=job_summary.entreprise,
                        description=self._clean_description(parsed["description"]),
                        source=self.source,
                        date_publication=parsed["date_publication"],
                        mode_travail=None,
                        competence=[],
                        duree_travail=None,
                        salaire=None,
                        formation=None,
                    )
                    logger.info(f"JobDetail: {jobdetail}")
                    return jobdetail
            return None
        except Exception as exc:
            print("Erreur dans extract_details", exc)
            raise

    def _clean_description(self, description: str) -> str:
        try:
            if not description:
                return ""
            clean_description: str = unescape(description)
            clean_description: str = BeautifulSoup(
                clean_description, "html.parser"
            ).get_text(separator=" ", strip=True)
            clean_description: str = " ".join([
                line.strip() for line in clean_description.splitlines() if line.strip()
            ])
            return clean_description
        except Exception as exc:
            logger.error(f"Erreur dans _clean_description: {exc}", exc_info=True)
            raise

    async def _fetch(self, url: str) -> str | List[str]:
        try:
            return await self.fetch.fetch(url)

        except asyncio.TimeoutError:
            raise Exception(f"Timeout lors de la requête pour url={url}")
        except Exception as e:
            raise Exception(f"Erreur lors du fetch: {str(e)}")
