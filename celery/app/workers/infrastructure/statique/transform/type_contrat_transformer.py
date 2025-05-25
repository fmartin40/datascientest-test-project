from typing import Any
from app.workers.interfaces.itransformer import ITransformer
import logging
from app.workers.entities.jobs import JobDetail
from app.core.nlp import get_nlp
from spacy.matcher import PhraseMatcher

logger = logging.getLogger(__name__)

class TypeContratTransformer(ITransformer):
    def __init__(self):
        self.contract_types: list[str] = []
        self._load_contract_types()

    async def transform(self, job_detail:JobDetail, llm:bool=False) -> JobDetail:
        if llm:
            job_detail.type_contrat = self._extract_keyword(job_detail.description)
        else:
            job_detail.type_contrat = self._extract_keyword(job_detail.description)
        return job_detail

    def _extract_keyword(self, texte: str) -> Any:
        nlp = get_nlp()
        doc = nlp(texte)
        keywords: list[str] = self._load_contract_types()
        matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
        patterns = [nlp.make_doc(text) for text in keywords]
        matcher.add("CIBLES", patterns)

        # Recherche des matches
        matches = matcher(doc)  
        found_keywords = [doc[start:end].text for match_id, start, end in matches]
        logger.info(f"Expressions trouvées : {found_keywords}")
        return found_keywords
    

    def _extract_llm(self, text: str) -> set:
        raise NotImplementedError("LLM extraction not implemented")

    def _load_contract_types(self) -> list[str]:
        return [
            "CDI",
            "CDD",
            "stage",
            "temporaire",
            "alternance",
        ]

    