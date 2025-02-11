from fastapi import APIRouter
from app.domain.pipelines.infra.extract.extract_nodriver import NoDriverExtract
from app.domain.pipelines.infra.extract.extract_plw import PlayWrightExtract
from app.domain.pipelines.infra.extract.http import HttptExtract
from app.domain.pipelines.infra.load.json.jobs_in_json import JobsInJsonRepo
from app.domain.pipelines.infra.transform.json_in_html_to_job import TransformJsonInHtmlToJob
from app.domain.pipelines.usecase.scrape_job_detail_usecase import ScrapJobDetailInputDto, ScrapJobDetailUseCase
from app.domain.pipelines.usecase.scrape_jobs_summaries_usecase import ScrapJobSummariesUseCase
from app.domain.pipelines.usecase.scrape_jobs_summaries_usecase import ScrapJobsSummariesInputDto


router = APIRouter(prefix="/pipelines", tags=["Pipelines temporaires"])

# ----------------------------------------------------
# ces endpoints sont temporaires et seront remplacés par un orchestrateurs


@router.post("/process/job/summaries")
async def process_jobs_summaries():

	return "En construction"
	# cette partie est temporaire et sera remplacée par les configuraton des sites à scrapper
	# on definira également une liste de mot clés à chercher pour les job

	# url_summaries: str ="https://www.jobintree.com/emploi/recherche.html?k={job}&l={place}"
	# query = url_summaries.format(job="data+engineer", place="paris")

	# input_dto = ScrapJobsSummariesInputDto(query = query, website="jobintree")

	# return await ScrapJobSummariesUseCase(
	# 	input_dto=input_dto,
	# 	extracter=PlayWrightExtract(),
	# 	transformer=TransformJsonInHtmlToJob(),
	# 	loader=JobsInJsonRepo(),
	# 	presenter=None,
	# ).execute()
	
@router.post("/process/job/detail")
async def process_job_detail():

	# cette partie est temporaire
	# on pourra récupérer l'url du job detail a scraper depuis une base ou un message kafka

	url: str = "https://www.jobintree.com/emplois/61665496.html" 
	website: str ="jobintree"

	url: str = "https://www.themuse.com/jobs/atlassian/senior-manager-data-science-6df833" 
	website: str ="muse"

	input_dto = ScrapJobDetailInputDto(url = url, website=website)

	return await ScrapJobDetailUseCase(
		input_dto=input_dto,
		extracter=HttptExtract(),
		transformer=TransformJsonInHtmlToJob(),
		loader=JobsInJsonRepo(),
		presenter=None,
	).execute()
	
