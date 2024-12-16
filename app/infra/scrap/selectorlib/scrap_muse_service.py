
import re
from typing import Dict, List
from glom import glom
from app.domain.scrap.entites.jobs import JobDetailled, JobSummary
from app.domain.scrap.interfaces.iscrape_service import IScrapeJob
from app.errors.errors import FetchApiException
from app.infra.scrap.selectorlib.fetch import FetchUrl


class ScrapMuseService(FetchUrl,IScrapeJob):
    def __init__(self):
        self.website_url:str = "https://www.themuse.com"
        self.job_summaries_url: str = "/api/search-renderer/jobs"
        self.job_detailled_url: str ="/jobs"


    async def __build_url(self, query: str, cursor: str | None = None)->Dict:
        query: str = re.sub(r"\s+", "+", query)
        params: str = (
            "?ctsEnabled=false"
            f"&query={query}"
            "&preference=krcbqorfvz"
            "&limit=20"
            "&timeout=5000"
        )
        if cursor:
            params+=f"&start_after={cursor}"
        
        return f"{self.website_url}{self.job_summaries_url}{params}"
        

    async def scrap_jobs_summaries(self, query: str, limit: int = 100, cursor: str | None = None)->List[JobSummary]:
        url:str = await self.__build_url(query, cursor)
        
        try:
            rslt: Dict = await self.fetch(url)
            
            if not rslt:
                return []
            
            job_specs = {
                "company": "hit.company.short_name",
                "job": "hit.short_title",
                "score": "score",
                "cursor": "cursor",
            }
            
            job_list: List[Dict] = [glom(job, job_specs) for job in rslt.get("hits")]
            job_list = sorted(job_list, key=lambda k: k["score"], reverse=True)
            job_summaries: List[JobSummary] = [
                JobSummary(
                    job=job.get('job'),
                    url= f"{self.website_url}{self.job_detailled_url}/{job.get('company')}/{job.get('job')}",
                    website="MUSE",
                    processed = False
                )
                for job in job_list
            ]
            return job_summaries
        except FetchApiException as exc:
            raise exc
        except Exception:
            raise
    
    async def scrap_job_content(self, url: str, website: str, *args, **kwargs)->List[JobDetailled]:
        raise NotImplementedError
