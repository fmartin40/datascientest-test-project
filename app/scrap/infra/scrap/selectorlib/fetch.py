import aiohttp

from app.scrap.errors.errors import FetchApiException


class FetchUrl:
    async def fetch(self, url: str):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url=url) as resp:
                    if resp.status < 300:
                        return await resp.json()
                    else :
                        raise FetchApiException(
                            status_code=resp.status,
                            message=resp.content
                        )
            except FetchApiException as fexc:
                raise fexc
            except Exception as exc:
                print(exc)
                raise
