from typing import List
from app.workers.common.entities.jobs import JobDetail
from app.workers.common.entities.settings import (
	ParserSettings,
	WebsiteInfo,
	WebsiteSettings,
)

from app.workers.common.interfaces.itransformer import ITransformer
from app.infrastructure.pipelines.extract.extractor_factory import ExtractorsFactory
from app.infrastructure.pipelines.transform.transformer_factory import TransformesrsFactory


class ScraperServices:
	def __init__(
		self, scrap_settings: WebsiteSettings
	):
		self.scrap_settings: WebsiteSettings = scrap_settings 
		self.website_info: WebsiteInfo = self.scrap_settings.website_info
		self.parsers: List[ParserSettings] = [parser for parser in self.scrap_settings.parsers if parser.actif]
		self.summary_extractor, self.detail_extractor = ExtractorsFactory.provide(self.parsers, self.website_info)
		
		transformer = next(parser for parser in self.parsers if parser.role == "transformer")
		self.transformer: ITransformer = TransformesrsFactory.provide(website_info=self.website_info, parser=transformer)

	async def extract_summarize(self, query: str, location:str, loop: int) -> str:
		try:
			print("Extractor summary: ", self.summary_extractor.__class__.__name__)
			return await self.summary_extractor.extract(query=query, location=location, loop=loop)
		except Exception as exc:
			print('get_summary_transformer : ', exc)
			raise
	
	async def extract_detail(self, url: str) -> str:
		print("Extractor detail : ", self.summary_extractor.__class__.__name__)
		return await self.detail_extractor.extract(url=url)

	async def transform(self, jobdetail: JobDetail):
		print("Transformer : ", self.transformer.__class__.__name__)
		return await self.transformer.transform(jobdetail)