from typing import List
from app.workers.entities.settings import ParserSettings, WebsiteInfo
from app.workers.interfaces.itransformer import ITransformer
from .keyword_transformer import KeywordTransformer
from .embedding_transformer import EmbeddingTransformer


class TransformersFactory:
    @staticmethod
    def provide(
        parsers: List[ParserSettings],
        website_info: WebsiteInfo,
    ) -> List[ITransformer]:
        """Renvoie la liste des transformers actifs selon les settings"""
        transformers: List[ITransformer] = []

        for parser in parsers:
            if parser.role == "transformer" and parser.actif:
                if parser.format == "keyword":
                    transformers.append(
                        KeywordTransformer(
                            website_info=website_info,
                            parser=parser,
                        )
                    )
                elif parser.format == "embenddings":
                    transformers.append(
                        EmbeddingTransformer(website_info=website_info, parser=parser)
                    )

        return transformers
