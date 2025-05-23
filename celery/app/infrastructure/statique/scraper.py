from typing import List
from app.workers.scrap.entities.jobs import JobSummary, JobDetail

from app.workers.scrap.interfaces.istatic_extractor import IStaticExtractor
from app.infrastructure.statique.extract.jobintree import JobInTreeExtractor
from app.infrastructure.statique.transform.competence_transformer import CompetencesTransformer
from app.infrastructure.statique.transform.type_contrat_transformer import TypeContratTransformer
from app.infrastructure.statique.transform.mode_trasnformer import ModeTransformer

class Scraper:
    def __init__(self, source: str):
        self.source: str = source
        self.extractor = self._provide(source)
        
    def _provide(self, source:str)->IStaticExtractor:
        """ Renvoie les transformers pour les format et type demandés"""
        match source:
            case "jobintree":
                extractor = JobInTreeExtractor()
            case _:
                raise ValueError(f"Source {source} non supportée")
        return extractor
    

    async def extract_summarize(
        self, query: str, location: str, loop: int
    ) -> List[JobSummary]:
        try:
            print("Extractor summary: ", self.extractor.__class__.__name__)
            return await self.extractor.extract_summaries(
                query=query, location=location, loop=loop
            )  # type: ignore
        except Exception as exc:
            print("get_summary_transformer : ", exc)
            raise

    async def extract_detail(self, url: str) -> List[JobDetail]:
        print("Extractor detail : ", self.extractor.__class__.__name__)
        return await self.extractor.extract_details(url=url)  # type: ignore

    async def transform(self, jobdetail: JobDetail) -> JobDetail:
        """Transforme les données du jobdetail"""
        jobdetail.competence = [] #await CompetencesTransformer().transform(jobdetail.description)
        jobdetail.type_contrat = "" #await TypeContratTransformer().transform(jobdetail.description)
        jobdetail.mode_travail = await ModeTransformer().transform(jobdetail.description)
        return jobdetail
