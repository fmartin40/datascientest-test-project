


import asyncio
import random
from typing import Dict, List
from aiohttp import ClientSession

from app.domain.pipelines.config.profiles import get_proxy, get_user_agent
from app.domain.pipelines.interfaces.ijob_extract import IJobExtract


class HttptExtract(IJobExtract):
    async def extract_jobs_summaries(self, url: str)->List[str]:
        return await self.fetch_all(urls=[url])
    
    async def extract_job_detail(self, url: str)->str:
        return await self.fetch_all(urls=[url])
    
    async def fetch_url(sel, session, url):
        """
        Récupère une URL en utilisant un sémaphore pour limiter les requêtes simultanées.
        """
        async with asyncio.Semaphore(5):  # Limiter le nombre de connexions simultanées
            try:
                async with session.get(url) as response:
                    data = await response.text()
                    print(f"Fetched {url} with status {response.status}")
                    return data
            except Exception as e:
                print(f"Error fetching {url}: {e}")
                return None


    async def fetch_all(self, urls: List[str]):
        """
        Récupère plusieurs URLs en parallèle avec un maximum de requêtes simultanées.
        """
        # Création d'une session HTTP partagée
        async with ClientSession() as session:
            tasks = [self.fetch_url(session, url) for url in urls]
            results = await asyncio.gather(*tasks)
            return results
    
