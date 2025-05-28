import asyncio
from typing import Dict, List, Optional, Union
import aiohttp
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)


class RequestConfig(BaseModel):
    method: str
    url: str
    payload: Optional[Dict]
    params: Optional[Dict]
    headers: Optional[Dict]


class HTTPStatusError(Exception):
    pass


class Fetch:
    def __init__(self, max_concurrent_requests: int = 10):
        """
        Initialize the Fetch class with a semaphore to control concurrent requests.

        Args:
            max_concurrent_requests (int): Maximum number of concurrent requests allowed
        """
        self.semaphore = asyncio.Semaphore(max_concurrent_requests)

    async def fetch(
        self, request_config: Union[RequestConfig, List[RequestConfig]]
    ) -> Union[Dict, List[Dict]]:
        """
        Make one or multiple HTTP requests.

        Args:
            request_config: Either a single RequestConfig or a list of RequestConfigs
                           Each RequestConfig should contain:
                           - method: HTTP method
                           - url: Endpoint URL
                           - payload: Optional request body
                           - params: Optional query parameters
                           - headers: Optional request headers

        Returns:
            Union[Dict, List[Dict]]: Single JSON response or list of JSON responses
        """
        try:
            async with aiohttp.ClientSession() as session:
                if isinstance(request_config, list):
                    # Multiple requests
                    tasks = [
                        self._make_request(
                            session,
                            req.method,  # type: ignore
                            req.url,  # type: ignore
                            req.payload,  # type: ignore
                            req.params,  # type: ignore
                            req.headers,  # type: ignore
                        )
                        for req in request_config
                    ]
                    return await asyncio.gather(*tasks)
                else:
                    # Single request
                    return await self._make_request(
                        session,
                        request_config.method,  # type: ignore
                        request_config.url,  # type: ignore
                        request_config.payload,  # type: ignore
                        request_config.params,  # type: ignore
                        request_config.headers,  # type: ignore
                    )
        except Exception as e:
            logger.error(f"Erreur lors de l'exécution de fetch : {e}")
            raise

    async def _make_request(
        self,
        session: aiohttp.ClientSession,
        method: str,
        url: str,
        payload: Optional[Dict] = None,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
    ) -> Dict:
        async with self.semaphore:
            try:
                async with session.request(
                    method=method, url=url, json=payload, params=params, headers=headers
                ) as response:
                    data = await response.json()
                    if response.status > 299:
                        raise HTTPStatusError(f"Erreur HTTP {response.status}: {data}")
                    return {"status_code": response.status, "data": data}
            except HTTPStatusError:
                raise  # Laisser remonter cette erreur personnalisée
            except Exception as e:
                logger.error(f"Erreur lors de la requête HTTP {method} {url} : {e}")
                raise  # Relever l'erreur générale aussi pour qu'elle soit captée au niveau supérieur
