import asyncio
import random
from typing import Dict, List
import nodriver as uc

from app.domain.pipelines.config.profiles import get_proxy, get_user_agent
from app.domain.pipelines.interfaces.ijob_extract import IJobExtract


class NoDriverExtract(IJobExtract):

	async def extract_jobs_summaries(self, url: str)->List[str]:
		raise NotImplementedError
	
	async def extract_job_detail(self, url: str)->str:
		browser = await uc.start(
			headless=False,
			lang="fr-FR",  # this could set iso-language-code in navigator, not recommended to change
		)
		page = await browser.get(url)
		html = await page.get_content()
		await browser.wait(2)
		await page.close()
		return html