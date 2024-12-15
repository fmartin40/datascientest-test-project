from dataclasses import dataclass

from app.domain.shared.abstract.usecase import IUseCase
from app.domain.shared.abstract.presenter import Presenter


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
			print(self.input_dto)
		except Exception as exc:
			raise Exception(exc)
