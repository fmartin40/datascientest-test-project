import asyncio
from aiohttp import ClientSession, ClientTimeout
from typing import List, Union, Optional

from app.domain.common.errors.errors import NotFoundException
from app.domain.pipelines.interfaces.ijob_extract import IJobExtract

# ---------------------------------------------------------
#   Cet extractor extrait le contenu d'une page
#           en faisant une requete http
# ---------------------------------------------------------


class HttptExtract(IJobExtract):
    def __init__(self):
        self.default_semaphore = asyncio.Semaphore(20)
        self.session_timeout = ClientTimeout(total=5,sock_connect=5,sock_read=5)

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

    async def _fetch_url(self, session:ClientSession, url: str, semaphore: asyncio.Semaphore) -> str:
        """ Télécharge le contenu des url """
        async with semaphore:
            try:
                async with session.get(url=url,timeout=self.session_timeout) as response:
                    if response.status<300:
                        return await response.text() 
                    elif response.status==404:
                        raise NotFoundException("L'url n'existe pas")
            except Exception as e:
                raise Exception(f"Erreur avec le fetch url : {e}")

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
