import asyncio
from typing import Dict, List, Union
from aiohttp import ClientSession, ClientTimeout, ClientError
import logging

logger = logging.getLogger(__name__)


class FetchUrl:
	def __init__(self, timeout=10):
		self.semaphore = asyncio.Semaphore(20)
		self.timeout = ClientTimeout(total=timeout)


	async def fetch(self, url: str) -> str:
		try:
			async with ClientSession(timeout=self.timeout) as session:
				return await self._fetch_url(session=session, url=url)
		except asyncio.TimeoutError:
			logger.error(f"Timeout lors de la requête pour url={url}")
			return ""
		except ClientError as e:
			logger.error(f"Erreur réseau lors de la requête pour url={url} : {e}")
			return ""
		except Exception as e:
			logger.error(f"Erreur inattendue lors de la requête pour url={url} : {e}")
			return ""


	async def multi_fetch(self, urls: List[str]) -> Union[str, List[Dict[str, str]]]:
		try:
			async with ClientSession(timeout=self.timeout) as session:
				tasks = [self._fetch_url(session, url) for url in urls]
				responses = await asyncio.gather(*tasks, return_exceptions=True)
			
			results = []
			for url, response in zip(urls, responses):
				if isinstance(response, Exception):
					results.append({"url": url, "error": str(response)})
				else:
					results.append({"url": url, "content": response})
			return results[0]["content"] if isinstance(urls, str) else results
		except Exception as exc:
			print("Erreur dans fetch", exc)
			raise


	async def _fetch_url(self, session: ClientSession, url: str) -> str:
		try:
			async with self.semaphore:
				async with session.get(url) as response:
					if response.status < 300:
						return await response.text()
					elif response.status == 404:
						raise Exception(f"404 Not Found: {url}")
					else:
						raise Exception(f"Failed to fetch {url}, status: {response.status}")
		except Exception as exc:
			print("Erreur dans _fetch_url", exc)
			raise
	
	