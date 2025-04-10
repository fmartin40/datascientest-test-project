


# Cette factory permet de remonter les differentes infra qui sont implémentées par les endpoint
# cela evite de reinitialiser les infra pour chaque endpoint et permet les changements à un seul endroit

from app.domain.pipelines.infra.extract.extract_http import HttptExtract
from app.domain.pipelines.infra.load.load_to_elastic import JobsInElastic
from app.domain.pipelines.infra.transform.json_in_html_to_job import TransformJsonInHtmlToJob
from app.domain.pipelines.infra.webconfig_json import WebConfigJson
from app.domain.pipelines.interfaces.ijob_extract import IJobExtract
from app.domain.pipelines.interfaces.ijob_load import IJobLoadToRepository
from app.domain.pipelines.interfaces.ijob_transform import IJobTransform
from app.domain.pipelines.interfaces.iconfig_service import IConfigService
from app.domain.reporting.infra.search_in_elastic import SearchInElastic
from app.domain.reporting.interfaces.ijob_search import IJobSearch


class InfraFactory:

	def get_webconfig_repo(self) -> IConfigService:
		return WebConfigJson()
		
	def get_extracter(self) -> IJobExtract:
		return HttptExtract()
		
	def get_transformer(self) -> IJobTransform:
		return TransformJsonInHtmlToJob()
		
	def get_loader(self) -> IJobLoadToRepository:
		return JobsInElastic()
	
	def get_job_search(self) -> IJobSearch:
		return SearchInElastic()
