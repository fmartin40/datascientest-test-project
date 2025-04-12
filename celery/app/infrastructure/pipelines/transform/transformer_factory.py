from app.workers.common.entities.settings import ParserSettings, WebsiteInfo
from app.workers.common.interfaces.itransformer import ITransformer
from app.infrastructure.pipelines.transform.llm_transformer import LLMTransformer

class TransformesrsFactory:
		
	@staticmethod
	def provide(website_info: WebsiteInfo, parser: ParserSettings)->ITransformer:
		""" Renvoie les transformers """
		
		return LLMTransformer(website_info=website_info, parser=parser)
		