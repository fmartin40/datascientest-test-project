import asyncio
from typing import List
from app.scrap.entites.jobs import JobSummary, JobDetailled
from app.scrap.infra.repositories.json.jobs_in_json import JobsInJsonRepo
from app.scrap.infra.scraper_factory import Website, get_scraper
from app.scrap.interfaces.iscrape_service import IJobScraper
from app.scrap.usecase.scrape_jobs_summaries_usecase import (
    ScrapJobSummariesUseCase,
    ScrapJobsSummariesInputDto,
)


async def scrape_job_summaries(website: Website, query: str) -> List[JobSummary]:
    scraper: IJobScraper = get_scraper(website)
    input_dto = ScrapJobsSummariesInputDto(query=query)
    return await ScrapJobSummariesUseCase(
        input_dto=input_dto,
        scraper=scraper,
        job_repository=JobsInJsonRepo(),
        presenter=None,
    ).execute()


if __name__ == "__main__":
    jobs: List[JobSummary] = asyncio.run(
        scrape_job_summaries(Website.MUSE, "data engineer")
    )
    print(jobs)
