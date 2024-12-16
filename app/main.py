import asyncio
from typing import List
from app.domain.scrap.entites.jobs import JobSummary, JobDetailled
from app.domain.scrap.interfaces.iscrape_service import IScrapeJob
from app.domain.scrap.usecase.scrape_jobs_summaries_usecase import (
    ScrapJobSummariesUseCase,
    ScrapJobsSummariesInputDto,
)


async def scrape_job_summaries(website: str, query: str) -> List[JobSummary]:
    input_dto: ScrapJobsSummariesInputDto = ScrapJobsSummariesInputDto(
        website=website, query=query
    )
    return await ScrapJobSummariesUseCase(input_dto=input_dto, presenter=None).execute()


if __name__ == "__main__":
    jobs: List[JobSummary] = asyncio.run(
        scrape_job_summaries("indeed", "data engineer")
    )
    print(jobs)
