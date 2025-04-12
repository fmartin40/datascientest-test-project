import re

from bs4 import BeautifulSoup

class TextUtils:
	@staticmethod
	def delete_spaces(html: str) -> str:
		return re.sub(r'\s+',' ', html)
	
	@staticmethod
	def html_to_text(html: str) -> str:
		return BeautifulSoup(html, 'html.parser').get_text(separator=" ", strip=True)