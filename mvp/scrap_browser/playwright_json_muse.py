import asyncio
from functools import lru_cache
import os
from pathlib import Path
from pprint import pprint
import random
import re
import aiohttp
from itertools import cycle
from typing import Dict, List, Tuple
from playwright.async_api import (
    Playwright,
    async_playwright,
    Locator,
    Page,
    Browser,
    BrowserType,
    BrowserContext,
)
import requests
from bs4 import BeautifulSoup
import json

from proxies import get_proxy, list_proxies, user_agents

async def init_browser(playwright: Playwright) -> Browser:
    browser: BrowserType = playwright.firefox if random.randint(0,100) % 2 else playwright.chromium
    return await browser.launch(headless=False)

async def init_context(browser: Browser, proxy: Dict, user_agent:str ) -> BrowserContext:
    context = await browser.new_context(user_agent=user_agent)
    await context.clear_cookies()
    return context

async def load_page(context: BrowserContext, landing_page: str, delay: int)->Page:
    page = await context.new_page()
    await page.goto(landing_page)
    # chargement de la page 
    await page.wait_for_load_state("domcontentloaded")
    
    await asyncio.sleep(delay)
    return page

async def extract_json(page: Page, tag)->Dict:
    html_content = await page.content()
    soup = BeautifulSoup(html_content, "html.parser")
    
    # 3️⃣ Trouver la balise <script> avec l'id __NEXT_DATA__
    script_tag = soup.find("script", tag)
    
    if script_tag:
        json_text = script_tag.string  # Récupérer le texte brut du script

        # 4️⃣ Charger le JSON en dictionnaire Python
        try:
            data = json.loads(json_text)
            print("✅ Données JSON extraites :", data)
            return data
        except json.JSONDecodeError as e:
            print("❌ Erreur lors du parsing JSON:", e)
    else:
        print("❌ Balise <script id='__NEXT_DATA__'> non trouvée")
    



async def main() -> None:
    proxy = await get_proxy()
    user_agent = random.choice(user_agents)
    ROOT_DIR = Path(__file__).parent.parent.parent
    EXTRACT_FOLDER = os.path.join(ROOT_DIR, "doc")
    
    url = "https://www.themuse.com/jobs/atlassian/senior-manager-data-science-6df833"
    file_name = "muse.json"
    tag= {"id": "__NEXT_DATA__"}
    
    async with async_playwright() as playwright:
        browser: Browser = await init_browser(playwright)
        context = await init_context(browser=browser, proxy=proxy, user_agent=user_agent)
        print()
        print()
        print("----------------- Browser", browser.browser_type)
        print("----------------- user_agent", user_agent)
        print("----------------- proxy", proxy)
        page = await load_page(context=context, landing_page=url, delay=5)
        data = await extract_json(page, tag)
        with open(f"{EXTRACT_FOLDER}/{file_name}", "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False) 
        
        pprint(data)
asyncio.run(main())
