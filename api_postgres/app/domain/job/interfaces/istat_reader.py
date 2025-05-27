from abc import ABC, abstractmethod
from typing import List, Any
from pydantic import BaseModel
from datetime import date


class IStatsReader(ABC):
    @abstractmethod
    async def list_competences_by_date(
        self, date_debut: date, date_fin: date
    ) -> List[BaseModel]:
        raise NotImplementedError

    async def get_competence_by_date(
        self, competence_id: int, date_debut: date, date_fin: date
    ) -> Any:
        raise NotImplementedError

    async def sum_competences_by_date(self, date_debut: date, date_fin: date) -> Any:
        raise NotImplementedError
