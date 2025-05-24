from typing import Any
from app.workers.scrap.interfaces.itransformer import ITransformer
import re
from rapidfuzz import process, fuzz
import logging
from app.workers.scrap.entities.jobs import JobDetail

logger = logging.getLogger(__name__)

class TypeContratTransformer(ITransformer):
    def __init__(self):
        self.contract_types: list[str] = []
        self._load_contract_types()

    def _extract_keyword(self, texte: str) -> Any:
        
        # Découpage du texte en phrases ou expressions
                
        # Découper le texte
        phrases = re.split(r"[.,;\n]", texte)
        phrases = [p.strip() for p in phrases if p.strip()]

        # Trouver le meilleur match pour chaque phrase
        scores = process.cdist(phrases, self.contract_types, scorer=fuzz.token_sort_ratio)
        for i, phrase in enumerate(phrases):
            for j, score in enumerate(scores[i]):
                if score > 85:
                    logger.info(f"→ '{phrase}' ≈ '{self.contract_types[j]}' (score: {score})")
        
        best_match = process.extractOne(texte, self.contract_types, scorer=fuzz.token_sort_ratio)
        logger.info(f"→ Meilleur match: {best_match}")
        return best_match[0] if best_match else ""

        # normalized_text: str = re.sub(
        #     r"[^a-z0-9\s]", " ", text.lower()
        # ).lower()
        # keyword: str = ""
        # for keyword in self.contract_types:
        #     normalized_keyword = re.sub(r"[^a-z0-9\s]", " ", keyword.lower()).strip()
        #     pattern = r"\b" + re.escape(normalized_keyword) + r"\b"
        #     if re.search(pattern, normalized_text):
        #         return keyword
        # return ""
    
    def _extract_llm(self, text: str) -> set:
        raise NotImplementedError("LLM extraction not implemented")

    def _load_contract_types(self) -> None:
        self.contract_types: list[str] = [
            "CDI",
            "CDD",
            "stage",
            "temporaire",
            "alternance",
        ]
        # return self.type_contrat

    async def transform(self, job_detail:JobDetail, llm:bool=False) -> JobDetail:
        if llm:
            job_detail.type_contrat = self._extract_keyword(job_detail.description)
        else:
            job_detail.type_contrat = self._extract_keyword(job_detail.description)
        return job_detail
