from dataclasses import dataclass

from app.domain.scrap.interfaces.iscrape_service import IScrapeJob
from app.domain.shared.abstract.usecase import IUseCase
from app.domain.shared.abstract.presenter import Presenter
from app.errors.errors import FetchApiException
from app.infra.scrap.selectorlib.scrap_muse_service import ScrapMuseService


@dataclass
class ScrapJobsSummariesInputDto:
	website: str
	query: str


class ScrapJobSummariesUseCase(IUseCase):
	def __init__(
		self,
		input_dto: ScrapJobsSummariesInputDto,
		presenter: Presenter | None = None,
	) -> None:
		super().__init__(presenter)
		self.input_dto = input_dto
		self.presenter = presenter

	async def execute(self):
		try:
			scraper: IScrapeJob = ScrapMuseService()
			return await scraper.scrap_jobs_summaries(self.input_dto.query)
		except FetchApiException as exc:
			raise exc
		except Exception as exc:
			raise Exception(exc)
