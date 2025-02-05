import asyncio
import random
from typing import Any, Dict, List
from playwright.async_api import (
    Playwright,
    async_playwright,
    Page,
    Browser,
    BrowserType,
    BrowserContext,
)
from bs4 import BeautifulSoup
import json

from app.domain.pipelines.config.profiles import get_proxy, get_user_agent
from app.domain.pipelines.entities.jobs import JobDetail, JobSummary
from app.domain.pipelines.entities.website import WebConfig
from app.domain.pipelines.interfaces.iscrape_service import IJobScraper


class PlayWrightScraper(IJobScraper):

    async def scrap_jobs_summaries(self, query: str, *args, **kwargs)->List[JobSummary]:
        raise NotImplementedError
    
    async def scrap_job_detail(self, url: str, webconfig: WebConfig)->JobDetail:
        proxy = await get_proxy()
        user_agent = random.choice(get_user_agent())
        
        async with async_playwright() as playwright:
            context: BrowserContext = self.__init_browser(playwright=playwright, proxy=proxy, user_agent=user_agent)
            print("----------------- Browser", context.browser)
            print("----------------- user_agent", user_agent)
            print("----------------- proxy", proxy)
            page = await self.__load_page(context=context, url=url, delay=5)
            content =  await self.__extract_json(page, webconfig.tag)
            return self.__parse_to_job_detail(content)
            
    async def __init_browser(self, playwright, proxy: Dict, user_agent:str) -> BrowserContext:
        browser: BrowserType = playwright.firefox if random.randint(0,100) % 2 else playwright.chromium
        instance: Browser = await browser.launch(headless=False)
        context: BrowserContext = await instance.new_context(user_agent=user_agent)
        await context.clear_cookies()
        return context
    
    async def __load_page(self, context: BrowserContext, url: str, delay: int)->Page:
        page = await context.new_page()
        await page.goto(url)

        # chargement de la page 
        await page.wait_for_load_state("domcontentloaded")
        await asyncio.sleep(delay)
        return page

    async def __extract_json(self, page: Page, tag: Any)->Dict:
        html_content = await page.content()
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Trouver la balise <script> avec l'id __NEXT_DATA__
        script_tag = soup.find("script", tag)
        
        if script_tag:
            json_text = script_tag.string  # Récupérer le texte brut du script

            # Charger le JSON en dictionnaire Python
            try:
                data = json.loads(json_text)
                print("Données JSON extraites :", data)
                return data
            except json.JSONDecodeError as e:
                print("Erreur lors du parsing JSON:", e)
        else:
            print(f"Balise <script {tag} non trouvée")
    
    async def __parse_to_job_detail(self, content: str)->JobDetail:
        return JobDetail(
            job="job",
            company="company",
            city = "city",
            url = "url",
            website="website",
            contenu="contenu"
        )
        


