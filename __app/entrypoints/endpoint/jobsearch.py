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
from app.domain.reporting.interfaces.ijob_search import IJobSearch
from app.entrypoints.dependencies import InfraFactory


router = APIRouter(prefix="/jobs", tags=["Recherche de job"])

# --------------------------------------------------------------------------
# ces endpoints sont temporaires et seront remplacés par un orchestrateur
# on utilise des endpoint pour lancer facilement le processus
# --------------------------------------------------------------------------


@router.get("/")
def search_job(
    infra: Annotated[InfraFactory, Depends(InfraFactory)],
    title: str | None = None,
    city: str | None = None,
    contract_type: str | None = None
):
    try:
        jobsearch: IJobSearch = infra.get_job_search()
        return jobsearch.search_jobs(title=title,city=city,contract_type=contract_type)
    except NotFoundException as ne:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ne))
    except FetchApiException as fe:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail=str(fe))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
