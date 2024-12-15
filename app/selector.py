import asyncio
from pprint import pprint
import aiohttp
from string import Template
from typing import List
from typing import Dict
import re
from itertools import cycle
from glom import glom
from dataclasses import dataclass, field
import asyncio
import aiohttp
from aiohttp import ClientSession
from selectorlib import Extractor
from elasticsearch import Elasticsearch

site_url: str = "https://www.themuse.com"
search_url: str = "/api/search-renderer/jobs"
job_url: Template = Template("/jobs/$company/$job_name")
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


# creation des Entités qui structurent les données et permettent une conservation en base
@dataclass
class JobSummary:
	company: str
	job_name: str
	url: str = field(init=False)
	processed: bool = False

	def __post_init__(self):
		self.url = job_url.safe_substitute(company=self.company, job_name=self.job_name)

@dataclass 
class JobMuse:
    company_size: str
    company_domain: List[str]
    contenu: str

    def __post_init__(self):
        self.company_size = re.sub(r'Size\:\s*','',self.company_size)
        industries: str = re.sub(r'Industry:\s*','',self.company_domain)
        self.company_domain = industries.split(',')


# requete de depart pour extraire la liste de jobs depuis une recherche
async def requests_for_jobs_summaries(query: str, cursor: str | None = None) -> List[Dict]:
	"""Effectue une requête pour lister les jobs.
			Dans le cas d'une pagination, on ajoute start_after= cursor du dernier job

	Args:
			query (str): requête dont les espaces sont remplacés par des +
			limit (int, optional): Limite de réponse max. Defaults à 20.
			cursor (str | None, optional): cursor à partir duquel est lancé la requete si pagination. Defaults to None.

	Returns:
			List[Dict]: liste des jobs
	"""
	query: str = re.sub(r"\s+", "+", query)
	search_params: Dict = {
		"ctsEnabled": "false",
		"query": query,
		"preference": "krcbqorfvz",
		"limit": 20,
		"timeout": 5000,
	}
	if cursor:
		search_params.update({"start_after": cursor})

	# proxy: str = random.choice(proxies)
	user_agent = next(cycle(user_agents))
	headers = {"User-Agent": user_agent, "Accept": "application/json"}
	url: str = f"{site_url}{search_url}"

	async with aiohttp.ClientSession() as session:
		try:
			async with session.get(
				url=url, params=search_params, headers=headers
			) as resp:
				if resp.status == 200:
					return await resp.json()

		except Exception as exc:
			print(exc)

# scrap des infos de base des summary de job
async def extract_summaries_infos(jobs_summaries: Dict) -> Dict:  # type: ignore
	"""Extrait les jobs a partir la reponse de l'api qui liste les jobs

	Args:
			jobs_summaries (Dict): dictionnaire renvoyé par l'api

	Returns:
			Dict: dictionnaire comprenant les différentes information résultant du scrap
	"""
	job_specs = {
		"company": "hit.company.short_name",
		"job_name": "hit.short_title",
		"score": "score",
		"cursor": "cursor",
	}
	job_list: List[Dict] = [glom(job, job_specs) for job in jobs_summaries.get("hits")]
	job_list = sorted(job_list, key=lambda k: k["score"], reverse=True)
	job_urls: List[JobSummary] = [
		JobSummary(company=job.get("company"), job_name=job.get("job_name"))
		for job in job_list
	]

	cursor: str = job_list[-1].get("cursor")
	has_more: bool = jobs_summaries.get("has_more", False)

	return dict(has_more=has_more, cursor=cursor, job_urls_ls=job_urls)


# requete de fetch pour l'asynchrone
# utilisé pour interroger les pages web des annonces
async def fetch_url(sem, session, url):
    """
    Récupère une URL en utilisant un sémaphore pour limiter les requêtes simultanées.
    """
    async with sem:  # Limiter le nombre de connexions simultanées
        try:
            async with session.get(url, timeout=10) as response:
                data = await response.text()
                print(f"Fetched {url} with status {response.status}")
                return data
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

async def fetch_all(urls: List[str], max_concurrent_requests: int=20):
    """
    Récupère plusieurs URLs en parallèle avec un maximum de requêtes simultanées.
    """
    # Initialisation du sémaphore
    sem = asyncio.Semaphore(max_concurrent_requests)
    
    # Création d'une session HTTP partagée
    async with ClientSession() as session:
        # Création des coroutines pour chaque URL
        tasks = [fetch_url(sem, session, url) for url in urls]
        
        # Exécution des tâches en parallèle
        results = await asyncio.gather(*tasks)
        return [rslt for rslt in results if rslt]


async def extract_all_urls_to_scrap():
	job_urls_ls: List[JobSummary] = []
	count: int = 0
	cursor: str | None = None
	query: str = "Data engineer"
	has_more: bool = True

	while has_more:
		# while count < 10:

		job_api_reponse: List[Dict] = await requests_for_jobs_summaries(query=query, cursor=cursor)
		scrap_result: Dict = await extract_summaries_infos(job_api_reponse)

		has_more: str = scrap_result.get("has_more")
		cursor: str = scrap_result.get("cursor")
		job_urls_ls.extend(scrap_result.get("job_urls_ls"))

		print(has_more)
		print(cursor)

		# simulation has_more=False apres 5 iterations
		count += 1
		if count > 2:
			has_more = False
		else:
			return job_urls_ls


def scrape_page(html: str, extractor: str):
    try:
        extractor = Extractor.from_yaml_file(extractor)
        # Appliquer les règles définies dans le fichier YAML
        data = extractor.extract(html)
        return data
    except Exception as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":

	# job_urls = asyncio.run(extract_all_urls_to_scrap())
	# print(len(job_urls))

	# urls = [f"{site_url}{job.url}" for job in job_urls]

	# results = asyncio.run(fetch_all(urls))
	# job_text_ls: List[JobMuse]=[JobMuse(**scrape_page(page,'rules_muse.yaml')) for page in results[:5]]
	# pprint(job_text_ls)

	client = Elasticsearch(hosts = "http://@localhost:9200")
	index = client.get(index="job", id="1")
	print(index)
