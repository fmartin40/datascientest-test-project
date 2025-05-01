from typing import Any, Dict, List
from app.workers.scrap.entities.settings import (
	ParserSettings,
	WebsiteInfo,
	WebsiteSettings,
)
from app.workers.scrap.entities.jobs import JobDetailInfos, JobSummary, JobDetail
from app.workers.scrap.interfaces.itransformer import ITransformer
from app.infrastructure.scrap.extract.extractor_factory import ExtractorsFactory
from app.infrastructure.scrap.transform.transformer_factory import TransformersFactory


class Scraper:
	def __init__(
		self, scrap_settings: WebsiteSettings
	):
		self.scrap_settings: WebsiteSettings = scrap_settings 
		self.website_info: WebsiteInfo = self.scrap_settings.website_info
		self.parsers: List[ParserSettings] = [parser for parser in self.scrap_settings.parsers if parser.actif]
		self.summary_extractor, self.detail_extractor = ExtractorsFactory.provide(self.parsers, self.website_info)
		
		self.transformers: List[ITransformer] = TransformersFactory.provide(
			website_info=self.website_info, 
			parsers=self.parsers,
		)

	async def extract_summarize(self, query: str, location:str, loop: int) -> List[JobSummary]:
		try:
			print("Extractor summary: ", self.summary_extractor.__class__.__name__)
			return await self.summary_extractor.extract(query=query, location=location, loop=loop) # type: ignore
		except Exception as exc:
			print('get_summary_transformer : ', exc)
			raise
	
	async def extract_detail(self, url: str) -> List[JobDetail]:
		print("Extractor detail : ", self.detail_extractor.__class__.__name__)
		return await self.detail_extractor.extract(url=url) # type: ignore

	async def transform(self, jobdetail: JobDetail)->JobDetail:
		print("Transformers : ", [transformer.__class__.__name__ for transformer in self.transformers])
		infos: Dict = {}
		for transformer in self.transformers:
			infos.update(await transformer.transform(jobdetail))
		jobdetail.infos = JobDetailInfos(**infos) # type: ignore
		return jobdetail