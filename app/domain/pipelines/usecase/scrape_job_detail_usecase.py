from dataclasses import dataclass
from typing import List

from app.domain.common.interface.presenter import Presenter
from app.domain.common.interface.usecase import IUseCase
from app.domain.pipelines.entities.jobs import JobSummary
from app.domain.pipelines.errors.errors import FetchApiException
from app.domain.pipelines.interfaces.ijob_extract import IJobExtract
from app.domain.pipelines.interfaces.ijob_transform import IJobTransform
from app.domain.pipelines.interfaces.ijob_load import IJobLoadToRepository


@dataclass
class ScrapJobDetailInputDto:
	url: str
	website: str

class ScrapJobDetailUseCase(IUseCase):
	def __init__(
		self,
		input_dto: ScrapJobDetailInputDto,
		extracter: IJobExtract,
		transformer: IJobTransform,
		loader: IJobLoadToRepository,
		presenter: Presenter | None = None,
	) -> None:
		super().__init__(presenter)
		self.input_dto = input_dto
		self.extracter = extracter
		self.transformer = transformer
		self.loader = loader
		self.presenter = presenter

	async def execute(self):
		try:

			raw_summaries: str = await self.extracter.extract_job_detail(self.input_dto.url)
			# summaries: List[JobSummary] = await self.transformer.transform_many(jobs=raw_summaries)
			# inserted: int = await self.loader.insert_many(summaries)
			
			return self.output(raw_summaries)  # type: ignore
		except FetchApiException:
			raise FetchApiException(errno = 10)
		except Exception as exc:
			raise Exception(exc)

	async def extract(self):
		pass

	async def transform(self):
		pass

	async def load(self):
		pass
	