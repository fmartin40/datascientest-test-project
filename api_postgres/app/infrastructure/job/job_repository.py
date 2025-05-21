import logging
from typing import Optional, Sequence
from pydantic import BaseModel
from app.domain.job.entities.jobs import Job
from app.domain.job.interfaces.ijob_repository import IJobRepository
from app.infrastructure.models.models import (
    OffreEmploiOrm,
    EntrepriseOrm,
    SalaireOrm,
    FormationOrm,
    LangueOrm,
    CompetenceOrm,
    SourceOrm,
    ModeTravailOrm,
    ExperienceOrm,
    DureeTravailOrm,
)
from app.domain.job.entities.jobs import (
    Source,
    Entreprise,
    Salaire,
    Experience,
    DureeTravail,
    ModeTravail,
    Formation,
    Langue,
    Competence,
)

from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.expressions import Q


EntreprisePydantic = pydantic_model_creator(EntrepriseOrm, name="Entreprise")
SalairePydantic = pydantic_model_creator(SalaireOrm, name="Salaire")
FormationPydantic = pydantic_model_creator(FormationOrm, name="Formation")
LanguePydantic = pydantic_model_creator(LangueOrm, name="Langue")
CompetencePydantic = pydantic_model_creator(CompetenceOrm, name="Competence")
SourcePydantic = pydantic_model_creator(SourceOrm, name="Source")
ModeTravailPydantic = pydantic_model_creator(ModeTravailOrm, name="ModeTravail")
ExperiencePydantic = pydantic_model_creator(ExperienceOrm, name="Experience")
DureeTravailPydantic = pydantic_model_creator(DureeTravailOrm, name="DureeTravail")

OffreEmploiPydantic = pydantic_model_creator(
    OffreEmploiOrm,
    name="OffreEmploiPydantic",
    include=(
        "source",  # Tortoise le mappe à .source automatiquement
        "entreprise",  # => entreprise
        "salaire",  # => salaire
        "experience",  # => experience
        "duree_travail",  # => duree_travail
        "mode_travail",  # => mode_travail
        "formations",  # M2M
        "langues",  # M2M
        "competences",  # M2M
    ),
)

logger = logging.getLogger(__name__)


class JobRepositoryPostgres(IJobRepository):
    async def add(self, job: Job) -> None:
        try:
            data = job.model_dump(exclude_unset=True)
            await OffreEmploiOrm.create(**data)
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout d'une offre d'emploi : {e}")
            raise

    async def list(
        self,
        competence: Optional[str] = None,
        langue: Optional[str] = None,
        formation: Optional[str] = None,
        entreprise: Optional[str] = None,
        type_contrat: Optional[str] = None,
    ) -> Sequence[Job]:
        try:
            query = OffreEmploiOrm.all().prefetch_related(
                "entreprise",
                "salaire",
                "source",
                "experience",
                "duree_travail",
                "mode_travail",
                "competences",
                "formations",
                "langues",
            )

            filters = Q()
            if competence:
                filters &= Q(competences__libelle__icontains=competence.lower())
            if langue:
                filters &= Q(langues__libelle__icontains=langue.lower())
            if formation:
                filters &= Q(formations__libelle__icontains=formation.lower())
            if entreprise:
                filters &= Q(entreprise__libelle__icontains=entreprise.lower())
            if type_contrat:
                filters &= Q(type_contrat__icontains=type_contrat.lower())

            if filters:
                query = query.filter(filters)

            offres = await query
            result = []
            for offre in offres:
                job = Job(
                    job_id=offre.job_id,
                    libelle=offre.libelle,
                    date_creation=offre.date_creation,
                    type_contrat=offre.type_contrat,
                    source=Source(**offre.source.__dict__) if offre.source else None,
                    entreprise=Entreprise(**offre.entreprise.__dict__)
                    if offre.entreprise
                    else None,
                    salaire=Salaire(**offre.salaire.__dict__)
                    if offre.salaire
                    else None,
                    experience=Experience(**offre.experience.__dict__)
                    if offre.experience
                    else None,
                    duree_travail=DureeTravail(**offre.duree_travail.__dict__)
                    if offre.duree_travail
                    else None,
                    mode_travail=ModeTravail(**offre.mode_travail.__dict__)
                    if offre.mode_travail
                    else None,
                    formations=[
                        Formation(**f.__dict__) for f in await offre.formations.all()
                    ],
                    langues=[Langue(**l.__dict__) for l in await offre.langues.all()],
                    competences=[
                        Competence(**c.__dict__) for c in await offre.competences.all()
                    ],
                )
                result.append(job)

            return result
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des offres d'emploi : {e}")
            return []

    async def get(self, job_id: str) -> Optional[BaseModel]:
        try:
            offre = (
                await OffreEmploiOrm.filter(id=job_id)
                .prefetch_related(
                    "entreprise",
                    "salaire",
                    "formations",
                    "langues",
                    "competences",
                    "source",
                )
                .first()
            )
            if not offre:
                return None
            job_pydantic = await OffreEmploiPydantic.from_tortoise_orm(offre)
            return job_pydantic
        except Exception as e:
            logger.error(
                f"Erreur lors de la récupération de l'offre d'emploi {job_id} : {e}"
            )
            return None

    async def delete(self, job_id: str) -> bool:
        try:
            deleted_count = await OffreEmploiOrm.filter(id=job_id).delete()
            return deleted_count > 0
        except Exception as e:
            logger.error(
                f"Erreur lors de la suppression de l'offre d'emploi {job_id} : {e}"
            )
            return False

    async def list_competences(self) -> Sequence[BaseModel]:
        try:
            return await CompetencePydantic.from_queryset(CompetenceOrm.all())
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des compétences : {e}")
            return []

    async def list_formations(self) -> Sequence[BaseModel]:
        try:
            return await FormationPydantic.from_queryset(FormationOrm.all())
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des formations : {e}")
            return []

    async def list_langues(self) -> Sequence[BaseModel]:
        try:
            return await LanguePydantic.from_queryset(LangueOrm.all())
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des langues : {e}")
            return []

    async def list_entreprises(self) -> Sequence[BaseModel]:
        try:
            return await EntreprisePydantic.from_queryset(EntrepriseOrm.all())
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des entreprises : {e}")
            return []

    async def list_salaires(self) -> Sequence[BaseModel]:
        try:
            return await SalairePydantic.from_queryset(SalaireOrm.all())
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des salaires : {e}")
            return []
