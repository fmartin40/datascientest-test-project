from dataclasses import dataclass

from app.domain.common.interface.presenter import Presenter
from app.domain.common.interface.usecase import IUseCase
from app.domain.pipelines.entities.jobs import JobDetail
from app.domain.pipelines.errors.errors import FetchApiException
from app.domain.pipelines.interfaces.ijob_summary_repo import IJobSummaryRepository
from app.domain.pipelines.interfaces.iscrape_service import IJobScraper


@dataclass
class ScrapJobDetailInputDto:
    url: str
    website: str


class ScrapJobDetailUseCase(IUseCase):
    def __init__(
        self,
        input_dto: ScrapJobDetailInputDto,
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
            # jobDetail: JobDetail = await self.scraper.scrap_job_detail(
            #     url=self.input_dto.url, website=self.input_dto.website
            # )
            return self.output("jobDetail")  # type: ignore
        except FetchApiException:
            raise FetchApiException(errno=10)
        except Exception as exc:
            raise Exception(exc)
