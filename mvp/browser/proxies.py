
from functools import lru_cache
import re
import aiohttp
from itertools import cycle
from typing import Dict, List

user_agents: List[str] = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Windows; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8",
        "Mozilla/5.0 (Windows NT 10.0; Windows; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Windows; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36",
    ]
@lru_cache
async def list_proxies(url: str)-> List[str]:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url=url) as resp:
                if resp.status == 200:
                    proxies_text = await resp.text()
                    proxies = proxies_text.split("\n")
                    return [
                        f"https://{proxy.split(':')[2]}:{proxy.split(':')[3]}@{proxy.split(':')[0]}:{proxy.split(':')[1]}"
                        for proxy in proxies
                        if proxy
                    ]
        except Exception as exc:
            print(exc)


async def get_proxy()->Dict[str, str]:
    proxies = await list_proxies("https://api.buyproxies.org/?a=showProxies&pid=141913&key=5c38699e3dd06dc81f32a2ce7e8bb091&port=12345")
    proxy_cycle = cycle(proxies)
    proxy = next(proxy_cycle)
    proxy_url = re.search(r'[0-9.:]+$', proxy).group(0)
    proxy_user = "webmaster"
    proxy_password = "wbemaster2016"
    return {
        "server": f"http://{proxy_url}",  # Adresse et port du proxy
        "username": proxy_user,          # Nom d'utilisateur
        "password": proxy_password       # Mot de passe
    }
