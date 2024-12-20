from dataclasses import dataclass
from typing import List

from app.scrap.entites.jobs import JobSummary
from app.scrap.interfaces.ijob_summary_repo import IJobSummaryRepository
from app.scrap.interfaces.iscrape_service import IJobScraper
from app.common.interface.usecase import IUseCase
from app.common.interface.presenter import Presenter
from app.scrap.errors.errors import FetchApiException


@dataclass
class ScrapJobsSummariesInputDto:
	query: str


class ScrapJobSummariesUseCase(IUseCase):
	def __init__(
		self,
		input_dto: ScrapJobsSummariesInputDto,
		scraper: IJobScraper,
		job_repository: IJobSummaryRepository,
		presenter: Presenter | None = None,
	) -> None:
		super().__init__(presenter)
		self.input_dto = input_dto
		self.scraper = scraper
		self.job_repository = job_repository
		self.presenter = presenter

	async def execute(self):
		try:
			jobs: List[JobSummary]  = await self.scraper.scrap_jobs_summaries(self.input_dto.query)
			await self.job_repository.create_many(jobs)
		except FetchApiException as exc:
			raise exc
		except Exception as exc:
			raise Exception(exc)
