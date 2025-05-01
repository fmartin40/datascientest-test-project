from typing import Any, Dict
from sentence_transformers import SentenceTransformer
from app.workers.scrap.entities.jobs import JobDetail
from app.workers.scrap.entities.settings import ParserSettings, WebsiteInfo
from app.workers.scrap.interfaces.itransformer import ITransformer

class EmbeddingTransformer(ITransformer):
    def __init__(self, website_info: WebsiteInfo, parser: ParserSettings):
        self.website_info: WebsiteInfo = website_info
        self.parser: ParserSettings = parser
        self.model = SentenceTransformer('quora-distilbert-multilingual')

    def _embeddings(self, job_description: str) -> list[float]:
        result = self.model.encode(job_description, show_progress_bar=False).tolist()
        return result

    async def transform(self, jobdetail: JobDetail) -> Dict[str, Any]:
        return {"embeddings":self._embeddings(jobdetail.description)} # type: ignore