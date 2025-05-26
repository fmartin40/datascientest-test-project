from app.workers.interfaces.itransformer import ITransformer
from spacy.matcher import PhraseMatcher
from typing import Literal, Dict, Any

import logging
from app.core.nlp import get_nlp


logger = logging.getLogger(__name__)

type_keyword = Literal["liste", "keyword"]

class MappingTransformer(ITransformer):
    def __init__(self, mapping: Dict[str, Any]):
        self.mapping = mapping

    async def transform(self, text: str, multi: bool = False) -> list[int] | int | None:
        """ 
        Extrait les mots clés d'un texte
        """
        nlp = get_nlp()
        doc = nlp(text)
        # Préparation du PhraseMatcher
        matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
        patterns = [nlp.make_doc(text) for text in list(self.mapping.keys())]
        matcher.add("CIBLES", patterns)
        matches = matcher(doc) # type: ignore
       
        if not matches:
            return None
        
        found_keywords = [doc[start:end].text for match_id, start, end in matches] # type: ignore
        
        if multi:
            matches: list[int] | None = [await self._map_id(keyword) for keyword in found_keywords] # type: ignore
            logger.info(f"matches: {matches}")
            return matches if matches else None
        else:
            return await self._map_id(found_keywords[0])
    
    async def _map_id(self, word: list[str] | str) -> list[int] | int | None:
        if isinstance(word, list):
            return [self.mapping[keyword.lower()] for keyword in word] # type: ignore
        elif isinstance(word, str):
            return self.mapping[word.lower()] # type: ignore
        else:
            return None