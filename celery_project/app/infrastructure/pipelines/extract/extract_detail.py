import json
from typing import List, Dict, Union
from glom import glom
from bs4 import BeautifulSoup
from app.workers.pipelines.entities.jobs import JobDetail
from app.workers.pipelines.entities.settings import ParserSettings, WebsiteInfo
from app.workers.pipelines.interfaces.iextractor import IExtractor
from app.infrastructure.pipelines.extract.fetchurl import FetchUrl


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

	async def extract(self, url: Union[str, List[str]]) -> JobDetail:
		try:
			content = await self.fetch.fetch(url)
			jsons = BeautifulSoup(content, 'html.parser').find_all('script', self.parser.json_tag)
			detail_required_json_keys: set = set(self.parser.json_required_keys)
			
			for js in jsons:
				json_to_parse: Dict = json.loads(js.string)
				if detail_required_json_keys.issubset(json_to_parse.keys()):
					parsed = glom(json_to_parse, self.parser.selectors)
					return JobDetail(**parsed, url=url, website=self.website_info.website, job_id="1")
		except Exception as exc:
			print("Erreur dans extract", exc)
			raise

	