from app.workers.scrap.interfaces.itransformer import ITransformer
from spacy.matcher import PhraseMatcher
from typing import Literal

import logging
from app.core.nlp import get_nlp

logger = logging.getLogger(__name__)

type_keyword = Literal["liste", "keyword"]

class KeywordTransformer(ITransformer):
    def __init__(self, keywords: list[str]):
        self.keywords = keywords


    async def transform(self, text: str, type: type_keyword) -> list[str] | str | None:
        """ 
        Extrait les mots clés d'un texte
        """
        if type == "liste":
            return self._extract_liste(text)
        elif type == "keyword":
            return self._extract_keyword(text)
        else:
            raise ValueError(f"Type de keyword invalide: {type}")   
    
    def _extract_liste(self, text: str) -> list[str]:
        nlp = get_nlp()
        doc = nlp(text)
        # Préparation du PhraseMatcher
        matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
        patterns = [nlp.make_doc(text) for text in self.keywords]
        matcher.add("CIBLES", patterns)

        # Recherche des matches
        matches = matcher(doc)
        found_keywords = [doc[start:end].text for match_id, start, end in matches]

        return found_keywords

    def _extract_keyword(self, text: str) -> str | None:
        nlp = get_nlp()
        doc = nlp(text)
        # Préparation du PhraseMatcher
        matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
        patterns = [nlp.make_doc(text) for text in self.keywords]
        matcher.add("CIBLES", patterns)

        # Recherche des matches
        matches = matcher(doc)
        found_keywords = [doc[start:end].text for match_id, start, end in matches]
        
        return found_keywords[0] if len(found_keywords) > 0 else None
    
    def _extract_llm(self, text: str) -> set:
        raise NotImplementedError("LLM extraction not implemented")

    