from dataclasses import dataclass
from typing import List

from app.domain.common.interface.presenter import Presenter
from app.domain.common.interface.usecase import IUseCase
from app.domain.pipelines.entities.jobs import JobSummary
from app.domain.pipelines.entities.extractconfig import ExtractConfig
from app.domain.common.errors.errors import FetchApiException
from app.domain.pipelines.interfaces.ijob_extract import IJobExtract
from app.domain.pipelines.interfaces.ijob_transform import IJobTransform
from app.domain.pipelines.interfaces.ijob_load import IJobLoadToRepository
from app.domain.pipelines.interfaces.iconfig_service import IConfigService


@dataclass
class ScrapJobsSummariesInputDto:
	query: str
	website: str

class ScrapJobSummariesUseCase(IUseCase):
	def __init__(
		self,
		input_dto: ScrapJobsSummariesInputDto,
		config_service: IConfigService,
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
		self.config_service = config_service
		self.presenter = presenter

	async def execute(self):
		try:
			# cette partie webconfig et l'objet renvoyé est purement temporaire et a definir.
			# l'idée est d'imaginer un obhjet config comprenant o;i de chose propre a chaque site
			# ex : pattern pour extraire les mots, format des url, balise html, fichier utilisé par selectorlib etc

			extract_config: ExtractConfig = self.config_service.get_website_config(name = self.input_dto.website)
			raw_summaries: List[str] = await self.extracter.extract_jobs_summaries(self.input_dto.query)
			summaries: List[JobSummary] = await self.transformer.transform_to_job_summaries(data=raw_summaries, extract_config=extract_config)
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
	