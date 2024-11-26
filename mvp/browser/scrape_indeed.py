import asyncio
from dataclasses import dataclass, field
from pprint import pprint
from typing import List
from  nodriver import * 
from selectorlib import Extractor

extractor = Extractor.from_yaml_file('rules_indeed.yaml')
#extractor = Extractor.from_yaml_file('rules_indeed_js.yaml')


@dataclass
class JobUrl:
    company: str
    job_name: str
    url: str 
    processed: bool = False

    def __post_init__(self):
        self.url = f"https://fr.indeed.com/{self.url}"

def scrape_page(html: str):
    try:
        # Appliquer les règles définies dans le fichier YAML
        data = extractor.extract(html)
        return data
    except Exception as e:
        print(f"Error: {e}")
        return None


async def open_browser():
    browser = await start(
        headless=False,
        lang="fr-FR"   # this could set iso-language-code in navigator, not recommended to change
    )
    page = await browser.get('https://fr.indeed.com/jobs?q=data+engineer')
    rslt = await page.get_content()
    await browser.wait(2)
    await page.close()
    return rslt
    
    

if __name__ == '__main__':

    rslt = asyncio.run(open_browser())
    jobs_ls: List = scrape_page(rslt)
    # jobs: List[JobUrl] = [JobUrl(**job) for job in jobs_ls['jobs']]
    pprint(jobs_ls)
