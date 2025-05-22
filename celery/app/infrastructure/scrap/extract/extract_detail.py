import json
from typing import Dict, Union
from glom import glom
from bs4 import BeautifulSoup
from app.workers.scrap.entities.jobs import JobDetail
from app.workers.scrap.entities.settings import ParserSettings, WebsiteInfo
from app.workers.scrap.interfaces.iextractor import IExtractor
from app.infrastructure.scrap.extract.fetchurl import FetchUrl


class JobDetailHTMLExtractor(IExtractor):
	def __init__(self, website_info: WebsiteInfo, parser: ParserSettings):
		self.website_info: WebsiteInfo = website_info
		self.parser: ParserSettings = parser
		self.fetch = FetchUrl()

	async def extract(self, url: str) -> Union[str, Dict[str, str]]:
		try:
			content = await self.fetch.fetch(url)
			soup = BeautifulSoup(content, 'html.parser')
			extracted_data = {}
			for key, selector in self.parser.selectors.items():
				element = soup.select_one(selector)
				extracted_data[key] = element.get_text(strip=True) if element else None
			return extracted_data
		except Exception as exc:
			print("Erreur dans extract", exc)
			raise

class JobDetailJSONExtractor(IExtractor):
	def __init__(self, website_info: WebsiteInfo, parser: ParserSettings):
		self.website_info: WebsiteInfo = website_info
		self.parser: ParserSettings = parser
		self.fetch = FetchUrl()

	async def extract(self, url:str) -> JobDetail|None:
		try:
			content = await self.fetch.fetch(url)
			jsons = BeautifulSoup(content, 'html.parser').find_all('script', self.parser.json_tag) # type: ignore
			detail_required_json_keys: set = set(self.parser.json_required_keys) # type: ignore
			
			if not jsons:
				return None
			for js in jsons:
				json_to_parse: Dict = json.loads(js.string) # type: ignore
				if detail_required_json_keys.issubset(json_to_parse.keys()):
					parsed = glom(json_to_parse, self.parser.selectors)
					return JobDetail(**parsed, url=url, website=self.website_info.website, job_id="1")
			return None
		except Exception as exc:
			print("Erreur dans extract", exc)
			raise

	