from typing import List
from itertools import chain
import urllib.parse
import asyncio
import logging

from bs4 import BeautifulSoup
from app.workers.infrastructure.dynamique.extract.fetchurl import FetchUrl
from app.workers.entities.jobs import JobSummary
from app.workers.entities.settings import ParserSettings, WebsiteInfo
from app.workers.interfaces.iextractor import IExtractor

logger = logging.getLogger(__name__)

class JobSummaryHTMLExtractor(IExtractor):
	def __init__(self, website_info: WebsiteInfo, parser: ParserSettings):
		self.website_info: WebsiteInfo = website_info
		self.parser: ParserSettings = parser
		self.fetch = FetchUrl()

	async def extract(self, query: str, location: str, loop: int) -> List[JobSummary]:
		try:
			content = await self._fetch(query=query, location=location, loop=loop)
			soup = BeautifulSoup(content, "html.parser") # type: ignore
			summaries: List[JobSummary] = []
			
			for selector in self.parser.selectors.values():
				elements = soup.select(selector)
				
				for el in elements:
					href:str = el.get("href") # type: ignore
					if href:
						logger.info(f"libelle: {el.get('libelle')}, entreprise: {el.get('entreprise')}, ville: {el.get('ville')}, type_contrat: {el.get('type_contrat')}")

						summaries.append(
							JobSummary(
								url=urllib.parse.urljoin(
									self.website_info.root_url, href
								),
								website=self.website_info.website,
								libelle=el.get("libelle"), # type: ignore
								source=self.website_info.website, # type: ignore
								entreprise=el.get("entreprise"), # type: ignore
								ville=el.get("ville"), # type: ignore
								type_contrat=el.get("type_contrat"), # type: ignore
							)
						)
			return summaries
		except Exception as exc:
			print("Erreur dans extract", exc)
			raise

	async def _fetch(self, query: str, location: str, loop: int) -> str | List[str]:
		request_url: str = self.website_info.request_url
		query = query.replace(" ", self.website_info.query_space_replacement)

		try:
			if loop == 1:
				url = request_url.format(query=query, location=location)
				url = urllib.parse.urljoin(self.website_info.root_url, url)
				content = await self.fetch.fetch(url)
			else:
				urls = []
				for i in range(2, loop + 1):
					paginated_url = request_url.format(query=query, location=location)
					paginated_url += f"&{self.parser.pagination}={i}"
					paginated_url = urllib.parse.urljoin(
						self.website_info.root_url, paginated_url
					)
					urls.append(paginated_url)

				contents = await self.fetch.multi_fetch(urls)
				content = list(chain.from_iterable(contents))
			return content
		except asyncio.TimeoutError:
			raise Exception(f"Timeout lors de la requête pour query={query}, location={location}")
		except Exception as e:
			raise Exception(f"Erreur lors du fetch: {str(e)}")


class JobSummaryJSONExtractor(IExtractor):
	def __init__(self, website_info: WebsiteInfo, parser: ParserSettings):
		self.website_info: WebsiteInfo = website_info
		self.parser: ParserSettings = parser
		self.fetch = FetchUrl()

	async def extract(self, query: str, location: str, loop: int) -> List[JobSummary]:
		try:
			raise NotImplementedError
			# content = await self._fetch(query=query, location=location, loop=loop)
			# jsons = BeautifulSoup(content, "html.parser").find_all(
			# 	"script", self.parser.json_tag
			# )
			# detail_required_json_keys: set = set(self.parser.json_required_keys)

			# for js in jsons:
			# 	json_to_parse: Dict = json.loads(js.string)
			# 	if detail_required_json_keys.issubset(json_to_parse.keys()):
			# 		return json_to_parse

		except Exception as exc:
			print("Erreur dans extract", exc)
			raise

	async def _fetch(self, query: str, location: str, loop: int) -> str | List[str]:
		request_url: str = self.website_info.request_url
		query = query.replace(" ", self.website_info.query_space_replacement)

		if loop == 1:
			url = request_url.format(query=query, location=location)
			url = urllib.parse.urljoin(self.website_info.root_url, url)
			content = await self.fetch.fetch(url)
		else:
			urls = []
			for i in range(2, loop + 1):
				paginated_url = request_url.format(query=query, location=location)
				paginated_url += f"&{self.parser.pagination}={i}"
				paginated_url = urllib.parse.urljoin(
					self.website_info.root_url, paginated_url
				)
				urls.append(paginated_url)

			contents = await self.fetch.multi_fetch(urls)
			content = list(chain.from_iterable(contents))
		return content
