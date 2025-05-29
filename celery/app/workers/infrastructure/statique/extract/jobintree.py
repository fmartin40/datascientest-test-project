from typing import List, Dict, Callable
import urllib.parse
from glom import glom
import asyncio
import logging
import json
from html import unescape
from bs4 import BeautifulSoup
from spacy.matcher import PhraseMatcher
from datetime import date, datetime
from app.workers.infrastructure.statique.extract.fetchurl import FetchUrl
from app.workers.entities.jobs import JobDetail, JobSummary
from app.workers.interfaces.istatic_extractor import IStaticExtractor
from app.core.nlp import get_nlp
from app.workers.interfaces.ikeyword_loader import IKeywordLoader

logger = logging.getLogger(__name__)


class JobInTreeExtractor(IStaticExtractor):
    def __init__(self, keywords_loader: IKeywordLoader):
        self.fetch = FetchUrl()
        self.source: str = "jobintree"
        self.base_url: str = "https://www.jobintree.com"
        self.request_url: str = "/emploi/recherche.html?k={query}&l={location}"
        self.keywords_loader: IKeywordLoader = keywords_loader
        self.type_contrat: Dict = {}
        self.duree_travail: Dict = {}
        self.competences: Dict = {}
        self.mode_travail: Dict = {}
        self.ville: Dict = {}
        # self.transformer: ITransformer = transformer

    async def extract_summaries(
        self, query: str, location: str, loop: int
    ) -> List[JobSummary]:
        try:
            await self._load_mappings()
            logger.info(f"type_contrat: {self.type_contrat}")
            logger.info(f"duree_travail: {self.duree_travail}")
            logger.info(f"competences: {self.competences}")
            logger.info(f"mode_travail: {self.mode_travail}")
            logger.info(f"ville: {self.ville}")
            url = urllib.parse.urljoin(
                self.base_url, self.request_url.format(query=query, location=location)
            )
            content = await self.fetch.fetch(url)
            soup = BeautifulSoup(content, "html.parser")  # type: ignore
            summaries: List[JobSummary] = []

            job_offers = soup.select("article.card-job-offer")

            for job_offer in job_offers:
                a_tag = job_offer.select_one("h3.no-marg a")
                if a_tag is None:
                    continue
                libelle = a_tag.get_text(strip=True)
                type_contrat = job_offer.select("li.job-criteria-label span")[
                    3
                ].get_text(strip=True)
                ville = job_offer.select("li.job-criteria-label span")[1].get_text(
                    strip=True
                )
                entreprise = job_offer.select("li.job-criteria-label span")[5].get_text(
                    strip=True
                )
                summaries.append(
                    JobSummary(
                        libelle=libelle if libelle else "nc",
                        url=urllib.parse.urljoin(self.base_url, a_tag.get("href")),  # type: ignore
                        source=self.source,
                        ville=ville if ville else location,
                        type_contrat=await self._transform(
                            type_contrat, self.type_contrat
                        ),  # type: ignore
                        entreprise=entreprise if entreprise else "nc",
                    )  # type: ignore
                )
            return summaries
        except asyncio.TimeoutError:
            raise Exception(f"Timeout lors de la requête pour url={url}")
        except Exception as exc:
            logger.error(f"Erreur dans extract_summaries: {exc}", exc_info=True)
            raise

    async def extract_details(
        self, job_summary: JobSummary, location: str
    ) -> JobDetail | None:
        try:
            json_to_parse = await self.extract_json(job_summary)

            if json_to_parse:
                selectors: dict = {
                    "description": "description",
                }
                parsed: Dict = glom(json_to_parse, selectors)  # type: ignore
                logger.info(f"Parsed from json: {parsed}")
            else:
                content = await self.fetch.fetch(job_summary.url)
                soup = BeautifulSoup(content, "html.parser")  # type: ignore
                div = soup.find("div", class_="container-small")
                description = div.get_text(strip=True) if div else ""
                parsed: Dict = {
                    "description": description,
                }
                logger.info(f"Parsed from html: {parsed}")

            # extraction des données depuis description
            if not job_summary.type_contrat:
                job_summary.type_contrat = await self._transform(parsed["description"], self.keywords_loader.load_type_contrat)  # type: ignore
            duree_travail: int = await self._transform(
                parsed["description"], self.duree_travail
            )  # type: ignore
            competence: list[int] = await self._transform(
                parsed["description"], self.competences, multi=True
            )  # type: ignore
            mode_travail: int = await self._transform(
                parsed["description"], self.mode_travail
            )  # type: ignore
            logger.info(f"voici la ville: {job_summary.ville}")
            logger.info(f"voici la location: {location}")
            if not job_summary.ville:
                job_summary.ville: str = await self._transform(  # type: ignore
                    job_summary.ville, self.ville
                )  # type: ignore
            else:
                job_summary.ville = location

            jobdetail = JobDetail(
                job_id="1",
                url=job_summary.url,
                libelle=job_summary.libelle,  # type: ignore
                date_creation=date.today().strftime("%Y-%m-%d"),
                ville=job_summary.ville,
                entreprise=job_summary.entreprise,
                description=self._clean_description(parsed["description"]),
                source=self.source,
                type_contrat=job_summary.type_contrat,
                mode_travail=mode_travail,
                competence=competence,
                duree_travail=duree_travail,
            )
            logger.info(f"JobDetail à insérer en base: {jobdetail}")
            return jobdetail
        except asyncio.TimeoutError:
            raise Exception(f"Timeout lors de la requête pour url={job_summary.url}")
        except Exception as exc:
            print("Erreur dans extract_details", exc)
            raise

    async def _load_mappings(self) -> None:
        self.type_contrat = await self.keywords_loader.load_type_contrat()
        self.duree_travail = await self.keywords_loader.load_duree_travail()
        self.competences = await self.keywords_loader.load_competences()
        self.mode_travail = await self.keywords_loader.load_mode_travail()
        self.ville = await self.keywords_loader.load_ville()

    async def extract_json(self, job_summary: JobSummary) -> Dict | None:
        try:
            if not job_summary.url.startswith(self.base_url):
                job_summary.url = urllib.parse.urljoin(self.base_url, job_summary.url)

            content: str = await self.fetch.fetch(job_summary.url)

            jsons = BeautifulSoup(content, "html.parser").find_all(
                "script", {"type": "application/ld+json"}
            )  # type: ignore

            if not jsons:
                return None

            for js in jsons:
                json_to_parse: Dict = json.loads(js.string)  # type: ignore
                if set(["description", "title"]).issubset(json_to_parse.keys()):
                    return json_to_parse

            return None
        except Exception as exc:
            logger.error(f"Erreur dans extract_json: {exc}", exc_info=True)
            raise

    def _clean_description(self, description: str) -> str:
        try:
            if not description:
                return ""
            clean_description: str = unescape(description)
            clean_description: str = BeautifulSoup(
                clean_description, "html.parser"
            ).get_text(separator=" ", strip=True)
            clean_description: str = " ".join(
                [
                    line.strip()
                    for line in clean_description.splitlines()
                    if line.strip()
                ]
            )
            return clean_description
        except Exception as exc:
            logger.error(f"Erreur dans _clean_description: {exc}", exc_info=True)
            raise

    async def _transform(
        self, text: str, mapping: Dict, multi: bool = False
    ) -> list[int] | int:
        """
        Extrait les mots clés d'un texte
        """
        logger.info(f"mapping fourni pour transform: {mapping}")
        if not mapping:
            return mapping.get("default")  # type: ignore
        extracted_keywords: list[str] | None = self._extract_keywords(
            text, mapping.get("mapping", {})
        )
        logger.info(f"extracted_keywords: {extracted_keywords}")

        if not extracted_keywords:
            return mapping.get("default")  # type: ignore

        mapped_to_id: list[int] = [
            mapping.get("mapping", {}).get(keyword.lower())
            for keyword in extracted_keywords
        ]  # type: ignore
        return mapped_to_id if multi else mapped_to_id[0]

    async def _find_keyword(self, keyword: str, load_keywords: Callable) -> str:
        """
        Retrouve le mot d'origine a partir d'un mot clé ex: paris 1er -> paris
        """
        mapping: Dict[str, Dict[str, str]] = await load_keywords()
        extracted_keywords: list[str] | None = self._extract_keywords(
            keyword, mapping.get("mapping", {})  # type: ignore
        )
        logger.info(f"extracted_keywords: {extracted_keywords}")

        if not extracted_keywords:
            return mapping.get("default")  # type: ignore

        found_keyword: str | None = mapping.get("mapping", {}).get(keyword.lower())
        return found_keyword if found_keyword else keyword

    def _extract_keywords(self, text: str, mapping: Dict[str, int]) -> list[str] | None:
        nlp = get_nlp()
        doc = nlp(text)
        # Préparation du PhraseMatcher
        matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
        patterns = [nlp.make_doc(text) for text in list(mapping.keys())]
        matcher.add("CIBLES", patterns)
        matches = matcher(doc)  # type: ignore

        if not matches:
            return None

        found_keywords = [doc[start:end].text for match_id, start, end in matches]  # type: ignore
        return found_keywords
