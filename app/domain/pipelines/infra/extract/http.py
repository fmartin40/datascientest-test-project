import asyncio
from aiohttp import ClientSession
from typing import List, Union, Optional

# ---------------------------------------------------------
#   Cet extractor extrait le contenu d'une page
#           en faisant une requete http
# ---------------------------------------------------------


class HttptExtract:
    def __init__(self):
        self.default_semaphore = asyncio.Semaphore(20)

    async def extract_jobs_summaries(self, url: str |List[str]) -> str | List[str]:
        """ Récupère un ou plusieurs contenus de page """
        return await self._fetch(url)

    async def extract_job_detail(self, url: str |List[str]) -> str | List[str]:
        """ Récupère un ou plusieurs contenus de page """
        return await self._fetch(url)

    async def _fetch(self, url: Union[str, List[str]]) -> Union[str, List[str]]:
        """ Détermine si l'on appelle une ou plusieurs urls"""
        if isinstance(url, list):
            return await self._fetch_all(url)
        async with ClientSession() as session:
            return await self._fetch_url(session, url, self.default_semaphore)

    async def _fetch_url(self, session, url: str, semaphore: asyncio.Semaphore) -> str:
        """ Télécharge le contenu des url """
        async with semaphore:
            try:
                async with session.get(url) as response:
                    data = await response.text()
                    return data
            except Exception as e:
                print(f"Error fetching {url}: {e}")
                return None

    async def _fetch_all(self, urls: List[str], max_concurrent_requests: Optional[int] = None) -> List[str]:
        """
        Récupère plusieurs URLs en parallèle avec semaphore.
        - Si `max_concurrent_requests` est spécifié, redéfini la taille du sémaphore.
        - Sinon, utilise le sémaphore par défaut.
        """
        semaphore = asyncio.Semaphore(max_concurrent_requests) if max_concurrent_requests else self.default_semaphore

        async with ClientSession() as session:
            tasks = [self._fetch_url(session, url, semaphore) for url in urls]
            return await asyncio.gather(*tasks)
