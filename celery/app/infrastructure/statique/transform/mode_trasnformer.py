from typing import Any
from app.workers.scrap.interfaces.itransformer import ITransformer
import logging
import spacy
from spacy.matcher import PhraseMatcher

logger = logging.getLogger(__name__)

class ModeTransformer(ITransformer):
    def __init__(self):
        self.keywords: list[str] = []
        self._load_keywords()

    def _extract_keyword(self, texte: str) -> Any:
        # Traitement avec spaCy
        nlp = spacy.load("fr_core_news_sm")
        doc = nlp(texte)

        # Préparation du PhraseMatcher
        matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
        patterns = [nlp.make_doc(text) for text in self.keywords]
        matcher.add("CIBLES", patterns)

        # Recherche des matches
        matches = matcher(doc)
        found_keywords = [doc[start:end].text for match_id, start, end in matches]

        # Afficher les extraits trouvés
        print("Expressions trouvées :", found_keywords)

        return found_keywords


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

    def _load_keywords(self) -> None:
        self.contract_types: list[str] = [
            "teletravail",
            "presentiel",
            "hybride",
            "remote",
            "partial remote",
            "hybrid",
            "flexible",    
        ]
        # return self.type_contrat

    async def transform(self, text:str, llm:bool=False) -> str:
        if llm:
            return ""
        else:
            return self._extract_keyword(text)
