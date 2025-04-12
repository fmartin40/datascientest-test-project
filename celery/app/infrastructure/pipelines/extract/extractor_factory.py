from typing import List

from app.workers.pipelines.entities.settings import ParserSettings, WebsiteInfo
from app.workers.pipelines.interfaces.iextractor import IExtractor
from app.infrastructure.pipelines.extract.extract_detail import JobDetailHTMLExtractor, JobDetailJSONExtractor
from app.infrastructure.pipelines.extract.extract_summaries import JobSummaryHTMLExtractor, JobSummaryJSONExtractor

class ExtractorsFactory:
		
	@staticmethod
	def provide(parsers: List[ParserSettings], website_info: WebsiteInfo)->List[IExtractor]:
		""" Renvoie les transformers pour les format et type demandés"""
		for parser in parsers:
			if parser.step == "summary":
				if parser.format == "html":
					summary = JobSummaryHTMLExtractor(website_info=website_info, parser=parser)
				if parser.format == "json":
					summary = JobSummaryJSONExtractor(website_info=website_info, parser=parser)
			if parser.step == "detail":
				if parser.format == "html":
					detail = JobDetailHTMLExtractor(website_info=website_info, parser=parser)
			if parser.step == "detail":
				if parser.format == "json":
					detail = JobDetailJSONExtractor(website_info=website_info, parser=parser)
		return summary, detail
	

