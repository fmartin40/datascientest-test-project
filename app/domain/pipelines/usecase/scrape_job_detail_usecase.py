from dataclasses import dataclass
from typing import Dict, List

from app.domain.common.interface.presenter import Presenter
from app.domain.common.interface.usecase import IUseCase
from app.domain.common.utils.uuid import generate_unique_id
from app.domain.pipelines.entities.jobs import JobDetail
from app.domain.pipelines.entities.webconfig import WebConfig
from app.domain.common.errors.errors import FetchApiException
from app.domain.pipelines.interfaces.ijob_extract import IJobExtract
from app.domain.pipelines.interfaces.ijob_transform import IJobTransform
from app.domain.pipelines.interfaces.ijob_load import IJobLoadToRepository
from app.domain.pipelines.interfaces.iweb_config import IWebconfig


@dataclass
class ScrapJobDetailInputDto:
    url: str
    website: str


class ScrapJobDetailUseCase(IUseCase):
    def __init__(
        self,
        input_dto: ScrapJobDetailInputDto,
        webconfig_repo: IWebconfig,
        extracter: IJobExtract,
        transformer: IJobTransform,
        loader: IJobLoadToRepository,
        presenter: Presenter | None = None,
    ) -> None:
        super().__init__(presenter)
        self.input_dto = input_dto
        self.webconfig_repo = webconfig_repo
        self.extracter = extracter
        self.transformer = transformer
        self.loader = loader
        self.presenter = presenter

    async def execute(self):
        try:
            # cette partie webconfig et l'objet renvoyé est purement temporaire et a definir.
            # l'idée est d'imaginer un objet config comprenant les configs propres a chaque site
            # ex : pattern pour extraire les mots, format des url, balise html, fichier utilisé par selectorlib etc
            webconfig: WebConfig = self.webconfig_repo.get_website_config(
                website=self.input_dto.website
            )

            # scrap des données en fonction du webconfig(json, html etc)
            html: str = await self.extracter.extract_job_detail(self.input_dto.url)

            # extration des données depuis la source et transformation en dictionnaire
            job: Dict = await self.transformer.transform_to_job_detail(
                data=html, webconfig=webconfig
            )

            inserted: Dict = {}
            if job:
                # creation objet JobDetail à partir du dictionnaire et des infos supplémentaires
                job_detail: JobDetail = JobDetail.create(
                    url=self.input_dto.url,
                    website=webconfig.name,
                    job_id=generate_unique_id(),
                    **job
                )
                inserted: int = await self.loader.insert(job=job_detail)

            return self.output(inserted)  # type: ignore
        except FetchApiException:
            raise FetchApiException(errno=10)
        except Exception as exc:
            raise Exception(exc)
