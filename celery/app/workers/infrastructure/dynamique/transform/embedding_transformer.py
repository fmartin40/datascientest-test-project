# from sentence_transformers import SentenceTransformer
from app.workers.interfaces.itransformer import ITransformer

# ce transformer est désactivé pour l'instant
    # la librairie sentence-transformers est trop lourde et ralentit la construction de l'image docker

class EmbeddingTransformer(ITransformer):
    pass
    # def __init__(self, website_info: WebsiteInfo, parser: ParserSettings):
    #     self.website_info: WebsiteInfo = website_info
    #     self.parser: ParserSettings = parser
    #     self.model = SentenceTransformer('quora-distilbert-multilingual')

    # def _embeddings(self, job_description: str) -> list[float]:
    #     result = self.model.encode(job_description, show_progress_bar=False).tolist()
    #     return result

    # async def transform(self, jobdetail: JobDetail) -> Dict[str, Any]:
    #     return {"embeddings":self._embeddings(jobdetail.description)} # type: ignore