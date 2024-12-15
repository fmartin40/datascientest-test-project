from dataclasses import dataclass
from datetime import date


@dataclass
class ToDateDto:
	"""utilisé pour les requetes qui nécessitent une date"""
	to_date: date


@dataclass
class FromDateDto:
	"""utilisé pour les requetes qui nécessitent une date"""
	to_date: date


@dataclass
class DateRangeDto:
	"""utilisé pour les requetes qui nécessitent des dates range"""
	from_date: date
	to_date: date


@dataclass
class LimitDto:
	"""utilisé pour les requetes qui renvoient des listes longues"""
	limit: int


@dataclass
class LimitOffsetDto:
	"""utilisé pour les requetes qui renvoient des listes longues"""
	limit: int
	offset: int


@dataclass
class DateRangeAndLimitOffsetDto(LimitOffsetDto, DateRangeDto):
	"""utilisé pour les requetes qui renvoient des listes longues"""
	pass


@dataclass
class DateRangeAndLimitDto(LimitDto, DateRangeDto):
	"""utilisé pour les requetes qui renvoient des listes longues"""
	pass

