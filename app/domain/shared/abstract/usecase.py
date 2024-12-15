from abc import abstractmethod
from typing import Any

from app.domain.shared.abstract.presenter import Presenter

class IUseCase:
	def __init__(self, presenter: Presenter | None) -> None:
		self.presenter = presenter
		
	async def execute(self, *args):
		raise NotImplementedError

	def output(self, output_dto):
		if not self.presenter:
			return output_dto
		else:
			return self.presenter.present(output_dto=output_dto)
 