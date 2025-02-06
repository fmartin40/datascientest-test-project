from fastapi import APIRouter
from app.domain.pipelines.infra.extract.extract_nodriver import NoDriverExtract
from app.domain.pipelines.infra.extract.extract_plw import PlayWrightExtract
from app.domain.pipelines.infra.load.json.jobs_summaries_in_json import JobsInJsonRepo
from app.domain.pipelines.infra.transform.json_in_html import TransformJsonInHtml
from app.domain.pipelines.usecase.scrape_job_detail_usecase import ScrapJobDetailInputDto, ScrapJobDetailUseCase
from app.domain.pipelines.usecase.scrape_jobs_summaries_usecase import ScrapJobSummariesUseCase
from app.domain.pipelines.usecase.scrape_jobs_summaries_usecase import ScrapJobsSummariesInputDto


router = APIRouter(prefix="/pipelines", tags=["Pipelines temporaires"])

@router.post("/process/summaries")
async def process_jobs_summaries():

	return "En construction"
	# cette partie est temporaire et sera remplacée par les configuraton des sites à scrapper
	# on definira également une liste de mot clés à chercher pour les job

	url_summaries: str ="https://www.jobintree.com/emploi/recherche.html?k={job}&l={place}"
	query = url_summaries.format(job="data+engineer", place="paris")

	input_dto = ScrapJobsSummariesInputDto(query = query, website="jobintree")

	return await ScrapJobSummariesUseCase(
		input_dto=input_dto,
		extracter=PlayWrightExtract(),
		transformer=TransformJsonInHtml(),
		loader=JobsInJsonRepo(),
		presenter=None,
	).execute()
	
@router.post("/process/detail")
async def process_job_detail():

	# cette partie est temporaire
	# on pourra récupérer l'url du job detai a scraper depuis une base ou un message kafka

	url_detail: str = "https://www.jobintree.com/emplois/60831578.html"
	
	input_dto = ScrapJobDetailInputDto(url = url_detail, website="jobintree")

	return await ScrapJobDetailUseCase(
		input_dto=input_dto,
		extracter=PlayWrightExtract(),
		transformer=TransformJsonInHtml(),
		loader=JobsInJsonRepo(),
		presenter=None,
	).execute()
	
