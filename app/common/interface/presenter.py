from abc import ABC, abstractmethod
from fastapi import Response


class Presenter(ABC):
	@abstractmethod
	def present(self, output_dto) -> Response:
		raise NotImplementedError
