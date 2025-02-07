import asyncio
import random
from typing import Dict, List

from playwright.async_api import (
    async_playwright,
	Playwright,
    Browser,
    BrowserType,
    BrowserContext,
)

from app.domain.pipelines.config.profiles import get_proxy, get_user_agent
from app.domain.pipelines.interfaces.ijob_extract import IJobExtract


class PlayWrightExtract(IJobExtract):

	async def extract_jobs_summaries(self, url: str)->List[str]:
		raise NotImplementedError
	
	async def extract_job_detail(self, url: str)->str:
		print('ddddddddddddddddddddddddddddddd')
		proxy = get_proxy()
		user_agent = random.choice(get_user_agent())
		
		async with async_playwright() as plw:
			context: BrowserContext = await self.__init_browser(plw=plw, proxy=proxy, user_agent=user_agent)
			page = await self.__load_page(context=context, url=url, delay=5)
			# print("----------------- Browser", context.browser)
			# print("----------------- user_agent", user_agent)
			# print("----------------- proxy", proxy)
			return page
			
	async def __init_browser(self, plw:Playwright, proxy: str, user_agent:str) -> BrowserContext:
		browser: BrowserType = plw.firefox if random.randint(0,100) % 2 else plw.chromium
		instance: Browser = await browser.launch(headless=True)
		context: BrowserContext = await instance.new_context(user_agent=user_agent)
		await context.clear_cookies()
		return context
	
	async def __load_page(self, context: BrowserContext, url: str, delay: int)->str:
		page = await context.new_page()
		await page.goto(url)

		# chargement de la page 
		await page.wait_for_load_state("domcontentloaded")
		await asyncio.sleep(delay)
		return await page.content()
	

	
