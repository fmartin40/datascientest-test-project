from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from app.domain.common.errors.errors import FetchApiException, NotFoundException
from app.domain.pipelines.usecase.scrape_job_detail_usecase import (
    ScrapJobDetailInputDto,
    ScrapJobDetailUseCase,
)
from app.domain.pipelines.usecase.scrape_jobs_summaries_usecase import (
    ScrapJobsSummariesInputDto,
)
from app.entrypoints.dependencies import InfraFactory


router = APIRouter(prefix="/pipelines", tags=["Pipelines temporaires"])

# --------------------------------------------------------------------------
# ces endpoints sont temporaires et seront remplacés par un orchestrateur
# on utilise des endpoint pour lancer facilement le processus
# --------------------------------------------------------------------------

@router.post("/process/job/summaries")
async def process_jobs_summaries(
    input_dto: Annotated[ScrapJobsSummariesInputDto, Depends(ScrapJobsSummariesInputDto)],
    infra: Annotated[InfraFactory, Depends(InfraFactory)],):
    return "En construction"
    # cette partie est temporaire et sera remplacée par les configuraton des sites à scrapper
    # on definira également une liste de mot clés à chercher pour les job

    # url_summaries: str ="https://www.jobintree.com/emploi/recherche.html?k={job}&l={place}"
    # query = url_summaries.format(job="data+engineer", place="paris")

    # input_dto = ScrapJobsSummariesInputDto(query = query, website="jobintree")

    # return await ScrapJobSummariesUseCase(
    # 	config_service=infra.get_webconfig_repo(),
	# 	extracter=infra.get_extracter(),
	# 	transformer=infra.get_transformer(),
	# 	loader=infra.get_loader(),
    # ).execute()


@router.post("/process/job/detail")
async def process_job_detail(
    infra: Annotated[InfraFactory, Depends(InfraFactory)],
    input_dto: ScrapJobDetailInputDto = Depends(),
):
    # cette partie est temporaire
    # on pourra récupérer l'url du job detail a scraper et le website
	# depuis une base ou un message kafka passé a l'api
	# exemple :
    #
    # url= "https://www.jobintree.com/emplois/61665496.html"
    # website = "jobintree"

    # url = "https://www.themuse.com/jobs/atlassian/senior-manager-data-science-6df833"
    # website = "muse"
    try: 
        return await ScrapJobDetailUseCase(
            input_dto=input_dto,
            config_service=infra.get_webconfig_repo(),
            extracter=infra.get_extracter(),
            transformer=infra.get_transformer(),
            loader=infra.get_loader()
        ).execute()
    except NotFoundException as ne:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ne))
    except FetchApiException as fe:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail=str(fe))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))