from fastapi import APIRouter
from app.domain.pipelines.infra.htttp.scrap_playwright import PlayWrightScraper
from app.domain.pipelines.infra.repositories.json.jobs_in_json import JobsInJsonRepo
from app.domain.pipelines.usecase.scrape_job_detail_usecase import ScrapJobDetailInputDto, ScrapJobDetailUseCase
from app.domain.pipelines.usecase.scrape_jobs_summaries_usecase import (
    ScrapJobSummariesUseCase,
    ScrapJobsSummariesInputDto,
)

router = APIRouter(prefix="/pipelines", tags=["Pipelines temporaires"])

@router.post("/jobs/summaries")
async def fetch_job_listings(input_dto: ScrapJobsSummariesInputDto):
    return await ScrapJobSummariesUseCase(
        input_dto=input_dto,
        scraper=PlayWrightScraper(),
        job_repository=JobsInJsonRepo(),
        presenter=None,
    ).execute()
    


@router.post("/jobs/details")
async def scrap_job_detail(input_dto: ScrapJobDetailInputDto):
    return await ScrapJobDetailUseCase(
        input_dto=input_dto,
        scraper=PlayWrightScraper(),
        job_repository=JobsInJsonRepo(),
        presenter=None,
    ).execute()
    
