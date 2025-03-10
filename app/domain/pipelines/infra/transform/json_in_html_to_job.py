import json
import re
from typing import Any, Dict, List
from bs4 import BeautifulSoup
from glom import glom, Coalesce
from app.domain.pipelines.entities.jobs import Job, JobDetail, JobSummary
from app.domain.pipelines.entities.extractconfig import ExtractConfig
from app.domain.pipelines.interfaces.ijob_transform import IJobTransform

# ---------------------------------------------------------
#   Ce transformer extrait le json d'une page html
#   pour en faire un objet structuré JobDetail
# ---------------------------------------------------------
class TransformJsonInHtmlToJob(IJobTransform):

	async def transform_to_job_summaries(self, data: str, extract_config: ExtractConfig)->List[JobSummary]:
		# required_keys: set = set(webconfig.summary_pattern.get('required'))
		# json_data = await self._extract_json(data, webconfig, required_keys)
		raise NotImplementedError

	async def transform_to_job_detail(self, data: str, extract_config: ExtractConfig)->JobDetail | List[JobDetail]:
		required_keys: set = set(extract_config.detail_pattern.get('required'))
		json_data: Dict = await self._extract_json(data, extract_config, required_keys)
		return await self._json_to_job_detail(json_data, extract_config)
	
	async def _extract_json(self, data: str, extract_config: ExtractConfig, required_keys: set) -> Dict:
		""" extraction du json a partir des infos webconfig """
		soup = BeautifulSoup(data, "html.parser")
		
		# Trouver la balise <script> avec le tag passé
		# si le json contient les clé attendues dans webconfig.detail_pattern.required, c'est le bon json
		# sinon on passe
		
		scripts = soup.find_all("script", extract_config.tag)
		for script in scripts:
			try:
				# On parse le json
				json_in_html = json.loads(script.string)  
				
				# si le resultat est un dict et et que ses clés contiennent nos required_keys on le retourne
				if isinstance(json_in_html, dict) and required_keys.issubset(json_in_html.keys()):
					return json_in_html  
			except (json.JSONDecodeError, TypeError):
				continue  # Ignore les erreurs (ex: script vide ou pas du JSON)
		
	async def _json_to_job_detail(self, json_data:Dict, extract_config: ExtractConfig )->JobDetail:
		# on utilise le pattern dans le webconfig pour en faire une specification glom
		# glom permet d'extraire des noeuds imbriques dans des dictionnaires 
		# {"title": "title", "company": "hiringOrganization.name"...}

		job_specs = {k:Coalesce(v,default='') for k, v in extract_config.detail_pattern.items() if k != 'required'}
		parsed_job: Dict = glom(json_data, job_specs)
		parsed_job['description']=await self._clean_description(parsed_job['description'])

		# Si les valeurs sont des liste, on les joint avec un |
		for k, v in parsed_job.items():
			if isinstance(v, list):
				parsed_job[k] = "|".join(map(str, v))
		return parsed_job
	
	async def _clean_description(self, html:Any)->str:
		if isinstance(html, list):
			html = " ".join(map(str, html))
		text = BeautifulSoup(html, "html.parser").get_text()
		return re.sub(r'\s+',' ', text)