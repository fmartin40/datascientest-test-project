import logging
from typing import Optional, Sequence
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from app.domain.job.entities.jobs import Job
from app.domain.job.interfaces.ijob_reader import IJobReader
from app.infrastructure.models.models import (
    OffreEmploiOrm,
    EntrepriseOrm,
    CompetenceOrm,
    SourceOrm,
    ModeTravailOrm,
    DureeTravailOrm,
    TypeContratOrm,
    VilleOrm,
)
from app.domain.job.entities.jobs import (
    Source,
    Entreprise,
    Ville,
    DureeTravail,
    ModeTravail,
    Competence,
    TypeContrat,
    JobLight,
)

from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.expressions import Q
from tortoise.queryset import QuerySet

EntreprisePydantic = pydantic_model_creator(EntrepriseOrm, name="Entreprise")
VillePydantic = pydantic_model_creator(VilleOrm, name="Ville")
CompetencePydantic = pydantic_model_creator(CompetenceOrm, name="Competence")
SourcePydantic = pydantic_model_creator(SourceOrm, name="Source")
ModeTravailPydantic = pydantic_model_creator(ModeTravailOrm, name="ModeTravail")
DureeTravailPydantic = pydantic_model_creator(DureeTravailOrm, name="DureeTravail")
TypeContratPydantic = pydantic_model_creator(TypeContratOrm, name="TypeContrat")

OffreEmploiPydantic = pydantic_model_creator(
    OffreEmploiOrm,
    name="OffreEmploiPydantic",
    include=(
        "job_id",
        "libelle",
        "date_creation",
        "url",
        "source",  # Tortoise le mappe à .source automatiquement
        "entreprise",  # => entreprise
        "duree_travail",  # => duree_travail
        "mode_travail",  # => mode_travail
        "type_contrat",  # => type_contrat
        "competences",  # M2M
    ),
)

logger = logging.getLogger(__name__)


class JobReader(IJobReader):
    async def add(self, job: Job) -> None:
        try:
            data = job.model_dump(exclude_unset=True)
            await OffreEmploiOrm.create(**data)
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout d'une offre d'emploi : {e}")
            raise

    async def list(
        self,
        limit: int,
        offset: int,
        competence: Optional[int] = None,
        entreprise: Optional[int] = None,
        ville: Optional[int] = None,
        type_contrat: Optional[int] = None,
        duree_travail: Optional[int] = None,
        mode_travail: Optional[int] = None,
        source: Optional[int] = None,
        light: bool = True,
    ) -> Sequence[Job | JobLight]:
        try:
            query = OffreEmploiOrm.all().prefetch_related(
                "entreprise",
                "ville",
                "source",
                "duree_travail",
                "mode_travail",
                "type_contrat",
                "competences",
            )

            filters = Q()
            if competence:
                filters &= Q(competences__id=competence)
            if entreprise:
                filters &= Q(entreprise__id=entreprise)
            if ville:
                filters &= Q(ville__id=ville)
            if type_contrat:
                filters &= Q(type_contrat__id=type_contrat)
            if duree_travail:
                filters &= Q(duree_travail__id=duree_travail)
            if mode_travail:
                filters &= Q(mode_travail__id=mode_travail)
            if source:
                filters &= Q(source__id=source)
            if filters:
                query = query.filter(filters).limit(limit).offset(offset)

            if light:
                return await self._get_light(query)
            else:
                return await self._get_full(query)
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des offres d'emploi : {e}")
            return []

    async def _get_light(self, query: QuerySet[OffreEmploiOrm]) -> Sequence[JobLight]:
        try:
            result = []
            offres = await query.values(
                "job_id",
                "libelle",
                "entreprise__id",
                "entreprise__libelle",
                "ville__id",
                "ville__libelle",
                "source__id",
                "source__libelle",
                "type_contrat__id",
                "type_contrat__libelle",
            )
            for offre in offres:
                entreprise = (
                    Entreprise(id=offre.get("entreprise__id"), libelle=offre.get("entreprise__libelle"))  # type: ignore
                    if offre.get("entreprise__id")
                    else None
                )
                ville = (
                    Ville(id=offre.get("ville__id"), libelle=offre.get("ville__libelle"))  # type: ignore
                    if offre.get("ville__id")
                    else None
                )  # type: ignore
                type_contrat = (
                    TypeContrat(id=offre.get("type_contrat__id"), libelle=offre.get("type_contrat__libelle"))  # type: ignore
                    if offre.get("type_contrat__id")
                    else None
                )  # type: ignore
                source = (
                    Source(id=offre.get("source__id"), libelle=offre.get("source__libelle"))  # type: ignore
                    if offre.get("source__id")
                    else None
                )  # type: ignore
                job = JobLight(
                    job_id=offre.get("job_id"),  # type: ignore
                    libelle=offre.get("libelle"),
                    type_contrat=type_contrat,  # type: ignore
                    entreprise=entreprise,  # type: ignore
                    ville=ville,  # type: ignore
                    source=source,  # type: ignore
                )
                result.append(job)
            return result
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des jobs légers : {e}")
            raise

    async def _get_full(self, query: QuerySet[OffreEmploiOrm]) -> Sequence[Job]:
        try:
            result = []
            offres = await query

            for offre in offres:
                entreprise = (
                    Entreprise(**offre.entreprise.__dict__)
                    if offre.entreprise
                    else None
                )  # type: ignore
                ville = (
                    Ville(**offre.ville.__dict__) if offre.ville else None
                )  # type: ignore
                type_contrat = (
                    TypeContrat(**offre.type_contrat.__dict__)
                    if offre.type_contrat
                    else None
                )  # type: ignore
                source = Source(**offre.source.__dict__) if offre.source else None  # type: ignore

                duree_travail = (
                    DureeTravail(**offre.duree_travail.__dict__)
                    if offre.duree_travail
                    else None
                )  # type: ignore
                mode_travail = (
                    ModeTravail(**offre.mode_travail.__dict__)
                    if offre.mode_travail
                    else None
                )  # type: ignore

                job = Job(
                    job_id=offre.job_id,
                    libelle=offre.libelle,
                    date_creation=offre.date_creation,
                    type_contrat=type_contrat,  # type: ignore
                    source=source,  # type: ignore
                    entreprise=entreprise,  # type: ignore
                    ville=ville,  # type: ignore
                    duree_travail=duree_travail,  # type: ignore
                    mode_travail=mode_travail,  # type: ignore
                    competences=[
                        Competence(**c.__dict__) for c in await offre.competences.all()
                    ],
                )
                result.append(job)

            return result
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des offres d'emploi : {e}")
            raise

    async def get(self, job_id: str) -> Optional[BaseModel]:
        try:
            query = OffreEmploiOrm.all().prefetch_related(
                "entreprise",
                "ville",
                "source",
                "duree_travail",
                "mode_travail",
                "type_contrat",
                "competences",
            )

            offre = await query.filter(Q(job_id=job_id)).first()

            if not offre:
                return None
            entreprise = (
                Entreprise(libelle=offre.entreprise.libelle, id=offre.entreprise.id)
                if offre.entreprise
                else None
            )  # type: ignore
            ville = (
                Ville(libelle=offre.ville.libelle, id=offre.ville.id)
                if offre.ville
                else None
            )  # type: ignore
            type_contrat = (
                TypeContrat(**offre.type_contrat.__dict__)
                if offre.type_contrat
                else None
            )  # type: ignore
            source = Source(libelle=offre.source.libelle, id=offre.source.id) if offre.source else None  # type: ignore

            duree_travail = (
                DureeTravail(
                    libelle=offre.duree_travail.libelle, id=offre.duree_travail.id
                )
                if offre.duree_travail
                else None
            )  # type: ignore
            mode_travail = (
                ModeTravail(
                    libelle=offre.mode_travail.libelle, id=offre.mode_travail.id
                )
                if offre.mode_travail
                else None
            )  # type: ignore

            job = Job(
                job_id=offre.job_id,
                libelle=offre.libelle,
                date_creation=offre.date_creation,
                type_contrat=type_contrat,  # type: ignore
                source=source,  # type: ignore
                entreprise=entreprise,  # type: ignore
                ville=ville,  # type: ignore
                duree_travail=duree_travail,  # type: ignore
                mode_travail=mode_travail,  # type: ignore
                competences=[
                    Competence(libelle=c.libelle, id=c.id)
                    for c in await offre.competences.all()
                ],
            )

            return job
        except Exception as e:
            logger.error(
                f"Erreur lors de la récupération de l'offre d'emploi {job_id} : {e}"
            )
            return None

    async def delete(self, job_id: str) -> bool:
        raise NotImplementedError("Not implemented")

    async def list_competences(self) -> Sequence[BaseModel]:
        try:
            return await CompetencePydantic.from_queryset(CompetenceOrm.all())
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des compétences : {e}")
            return []

    async def list_entreprises(self) -> Sequence[BaseModel]:
        try:
            return await EntreprisePydantic.from_queryset(EntrepriseOrm.all())
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des entreprises : {e}")
            return []

    async def list_type_contrat(self) -> Sequence[BaseModel]:
        try:
            return await TypeContratPydantic.from_queryset(TypeContratOrm.all())
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des types de contrat : {e}")
            return []

    async def list_duree_travail(self) -> Sequence[BaseModel]:
        try:
            return await DureeTravailPydantic.from_queryset(DureeTravailOrm.all())
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des durées de travail : {e}")
            return []

    async def list_mode_travail(self) -> Sequence[BaseModel]:
        try:
            return await ModeTravailPydantic.from_queryset(ModeTravailOrm.all())
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des modes de travail : {e}")
            return []

    async def list_source(self) -> Sequence[BaseModel]:
        try:
            return await SourcePydantic.from_queryset(SourceOrm.all())
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des sources : {e}")
            return []
