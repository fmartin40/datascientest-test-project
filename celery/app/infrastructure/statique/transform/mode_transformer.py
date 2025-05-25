from typing import Any
from app.workers.scrap.interfaces.itransformer import ITransformer
import logging
import spacy
from spacy.matcher import PhraseMatcher
from app.workers.scrap.entities.jobs import JobDetail
from app.core.nlp import get_nlp
logger = logging.getLogger(__name__)

class ModeTravailTransformer(ITransformer):
    def __init__(self):
        self.keywords: list[str] = []
        self._load_keywords()


    async def transform(self, job_detail:JobDetail, llm:bool=False) -> JobDetail:
        if llm:
            job_detail.mode_travail = self._extract_keyword(job_detail.description)
        else:
            job_detail.mode_travail = self._extract_keyword(job_detail.description)
        return job_detail


    def _extract_keyword(self, text: str) -> Any:
        nlp = get_nlp()
        doc = nlp(text)
        keywords: list[str] = self._load_keywords()
        # Préparation du PhraseMatcher
        matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
        patterns = [nlp.make_doc(text) for text in keywords]
        matcher.add("CIBLES", patterns)

        # Recherche des matches
        matches = matcher(doc)
        found_keywords = [doc[start:end].text for match_id, start, end in matches]

        # Afficher les extraits trouvés
        logger.info(f"Expressions trouvées : {found_keywords}")
        return found_keywords


    
    def _extract_llm(self, text: str) -> set:
        raise NotImplementedError("LLM extraction not implemented")

    def _load_keywords(self) -> list[str]:
        return [
            "teletravail",
            "presentiel",
            "hybride",
            "remote",
            "partial remote",
            "hybrid",
            "flexible",    
        ]

    