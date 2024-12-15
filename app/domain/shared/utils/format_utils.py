import calendar
from datetime import date
from dateutil.relativedelta import relativedelta
import numpy as np

class FormatUtils:
	@staticmethod
	def time_to_text(seconds: int | float) -> str:
		if not seconds:
			return ''
		try:
			minute, seconde = divmod(round(seconds, ndigits=2), 60)  # type: ignore
			seconde = f'0{round(seconde)}' if seconde < 10 else round(seconde)
			return f"{round(minute)}'{seconde}''"  # type: ignore
		except Exception as exc:
			print('erreur time to text :', exc)
			return ''

	@staticmethod
	def datediff_to_periode(from_date:date, to_date:date) -> relativedelta:
		return relativedelta(to_date, from_date)
	
	@staticmethod
	def is_monthly_daterange(from_date: date, to_date: date) -> bool:
		# si l'annee et le mois de from_date et to_date sont identiques
		# on verifie si le jour de from_date et le 1
		# dans ce cas on verifie si le jour de to_date est le dernier jour du mois
		# si c'est le cas, le rapport sera stocke dans monthly_report
		is_monthly: bool = False
		
		if from_date.year == to_date.year:
			if from_date.month == to_date.month:
				if from_date.day == 1:
					last_day = calendar.monthrange(from_date.year, from_date.month)[1]
					if to_date.day == last_day:
						is_monthly = True

		return is_monthly
	
	@staticmethod
	def get_last_day_month(year: int, month: int) -> bool:
		return calendar.monthrange(year, month)[1] # type: ignore
	
	@staticmethod
	def generate_monthly_date_ranges(from_year: int, from_month: int, to_year: int, to_month: int):
		current_year = from_year
		current_month = from_month
		date_ranges = []

		while (current_year, current_month) <= (to_year, to_month):
			start_date = date(current_year, current_month, 1) # type: ignore
			end_date = date(current_year, current_month, calendar.monthrange(current_year, current_month)[1]) # type: ignore
			date_ranges.append((start_date, end_date))
			
			# Increment month
			if current_month == 12:
				current_month = 1
				current_year += 1 # type: ignore
			else:
				current_month += 1

		return date_ranges