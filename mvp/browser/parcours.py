import asyncio
from functools import lru_cache
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

from proxies import get_proxy, list_proxies, user_agents

async def init_browser(playwright: Playwright) -> Browser:
    browser: BrowserType = playwright.firefox if random.randint(0,100) % 2 else playwright.chromium
    return await browser.launch(headless=False)

async def init_context(browser: Browser, proxy: Dict, user_agent:str ) -> BrowserContext:
    context = await browser.new_context(user_agent=user_agent)
    await context.clear_cookies()
    return context

async def scrap_page(context: BrowserContext, landing_page: str, delay: int)->Page:
    page = await context.new_page()
    await page.goto(landing_page)
    # chargement de la page 
    await page.wait_for_load_state("domcontentloaded")
    html = await page.content()
    print(html)
    await asyncio.sleep(delay)
    return page

# async def stop_loop(browser: Browser, context: BrowserContext)->None:
#     await context.close()
#     await browser.close()
    
# async def add_idx_to_links_js(page:Page)->None:
#     return await page.evaluate("""
#         var links = document.getElementsByTagName("a");
#         var liens = [];
#         for (var i = 0; i < links.length; i++) {
#             var href = links[i].href;
#             if (
#                 href.includes('worldtempus.com/article/') || 
#                 href.includes('worldtempus.com/montres/') || 
#                 href.includes('worldtempus.com/watches/')
#             ) {
#                 if (href.endsWith('.html')) {
#                     var ajout_tag = 'idx=1';
#                     if (href.includes('?')) {
#                         links[i].href = href + '&' + ajout_tag;
#                     } else {
#                         links[i].href = href + '?' + ajout_tag;
#                     }
#                     liens.push(links[i].href);
#                 }
#             }
#         }
#         """)

async def extract_articles_and_watches_links(page: Page) -> Tuple[List[Locator], List[Locator]]:
    try:
        # extraction des liens
        links = await page.get_by_role("link").all()

        if not links:
            raise Exception("Aucun lien correspondant trouvé.")

        links_article: List[Locator] = []
        links_watches: List[Locator] = []

        for link in links:
            href: str = await link.get_attribute("href")
            if re.search("worldtempus.com/article/.*\.html", href):
                links_article.append(link)
            if re.search("worldtempus.com/montres/.*\.html|worldtempus.com/watches/.*\.html", href):
                links_watches.append(link)
        return links_article, links_watches
    except Exception as e:
        raise e

# def get_domain(langue: str)->str:
#      return "https://fr.worldtempus.com" if langue == "fr" else "https://en.worldtempus.com"
        
# async def goto_page_and_pause(page:Page, delay:int) -> Page:
#     try:
#         # ajout idx=1 aux urls
#         # await add_idx_to_links_js(page)
#         links_article, links_watches = await extract_articles_and_watches_links(page)
        
#         # extraction d'un lien article ou montre et clic
#         link_article = random.choice(links_article)
#         await link_article.click()

#         # chargement de la page + pause sur la page le temps du delay
#         print("chargement de la page et pause", page.url )
#         await page.wait_for_load_state("domcontentloaded")
#         await asyncio.sleep(delay)
#         return page
#         # await page.pause()

#     except Exception as e:
#         print(e)

# async def launch_loop(browser: Browser, context: BrowserContext, nb_pages: int, delay:int)->None:
#     page = await start_loop_and_pause(context=context, langue="fr", landing_page="https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwje4Pne3IGCAxU71wIHHbJfBaEQFnoECA4QAQ&url=https%3A%2F%2Ffr.worldtempus.com%2Fboutiques-de-montre%2Farije-6&usg=AOvVaw3mWry8B81-d7vbXMH3wyK2&opi=899784493", delay=5)
#     page = await goto_page_and_pause(page=page, delay=5)
#     page = await goto_page_and_pause(page=page, delay=5)
#     await stop_loop(browser=browser,context=context)

async def main() -> None:
    proxy = await get_proxy()
    user_agent = random.choice(user_agents)
    
    async with async_playwright() as playwright:
        browser: Browser = await init_browser(playwright)
        context = await init_context(browser=browser, proxy=proxy, user_agent=user_agent)
        print()
        print()
        print("----------------- Browser", browser.browser_type)
        print("----------------- user_agent", user_agent)
        print("----------------- proxy", proxy)
        page = await scrap_page(context=context, landing_page="https://fr.indeed.com/", delay=10)
    
        # await launch_loop(browser=browser, context=context, nb_pages = 3, delay = 5)

asyncio.run(main())
