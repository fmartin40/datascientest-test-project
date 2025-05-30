from abc import ABC, abstractmethod
from typing import List, Any
from pydantic import BaseModel
from datetime import date


class IStatsReader(ABC):
    @abstractmethod
    async def list_competences_by_day(
        self, from_date: date, to_date: date
    ) -> List[BaseModel]:
        raise NotImplementedError

    async def sum_competences_by_date(
        self, from_date: date, to_date: date, competence_id: int | None = None
    ) -> Any:
        raise NotImplementedError

    @abstractmethod
    def get_competence_by_ville(self, ville_id: int) -> Any:
        raise NotImplementedError
