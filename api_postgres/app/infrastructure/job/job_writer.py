from app.infrastructure.schemas.job_insert import JobCreate, EntrepriseCreate, SalaireCreate, FormationCreate, LangueCreate, ExperienceCreate, DureeTravailCreate, CompetenceCreate, ModeTravailCreate, TypeContratCreate, SourceCreate
from app.domain.job.interfaces.ijob_writer import IJobWriter  
from app.infrastructure.models.models import (
    EntrepriseOrm, SalaireOrm, FormationOrm, LangueOrm, ExperienceOrm,
    DureeTravailOrm, CompetenceOrm, ModeTravailOrm, TypeContratOrm,
    SourceOrm, OffreEmploiOrm
)

class JobWriter(IJobWriter):
    async def add(self, job: JobCreate) -> None:
        offre = await OffreEmploiOrm.create(
            job_id=job.job_id,
            date_creation=job.date_creation,
            libelle=job.libelle,
            entreprise_id=job.entreprise_id,
            ville_id=job.ville_id,
            salaire_id=job.salaire_id,
            source_id=job.source_id,
            experience_id=job.experience_id,
            duree_travail_id=job.duree_travail_id,
            mode_travail_id=job.mode_travail_id,
            type_contrat_id=job.type_contrat_id,
        )
        if job.competence_ids:
            await offre.competences.add(*job.competence_ids)
        if job.langue_ids:
            await offre.langues.add(*job.langue_ids)
        if job.formation_ids:
            await offre.formations.add(*job.formation_ids)

    async def delete(self, job_id: str) -> bool:
        deleted_count = await OffreEmploiOrm.filter(job_id=job_id).delete()
        return deleted_count > 0

    async def add_entreprise(self, entreprise: EntrepriseCreate) ->  EntrepriseOrm:
        return await EntrepriseOrm.get_or_create(libelle=entreprise.libelle) # type: ignore

    async def add_salaire(self, salaire: SalaireCreate) -> SalaireOrm:
        return await SalaireOrm.get_or_create(libelle=salaire.libelle) # type: ignore

    async def add_formation(self, formation: FormationCreate) -> FormationOrm:
        return await FormationOrm.get_or_create(libelle=formation.libelle) # type: ignore

    async def add_langue(self, langue: LangueCreate) -> LangueOrm:
        return await LangueOrm.get_or_create(libelle=langue.libelle) # type: ignore

    async def add_experience(self, experience: ExperienceCreate) -> ExperienceOrm:
        return await ExperienceOrm.get_or_create(libelle=experience.libelle) # type: ignore

    async def add_duree_travail(self, duree_travail: DureeTravailCreate) -> DureeTravailOrm:
        return await DureeTravailOrm.get_or_create(libelle=duree_travail.libelle) # type: ignore

    async def add_competence(self, competence: CompetenceCreate) -> CompetenceOrm:
        return await CompetenceOrm.get_or_create(libelle=competence.libelle) # type: ignore

    async def add_mode_travail(self, mode_travail: ModeTravailCreate) -> ModeTravailOrm:
        return await ModeTravailOrm.get_or_create(libelle=mode_travail.libelle) # type: ignore

    async def add_type_contrat(self, type_contrat: TypeContratCreate) -> TypeContratOrm:
        return await TypeContratOrm.get_or_create(libelle=type_contrat.libelle) # type: ignore

    async def add_source(self, source: SourceCreate) -> SourceOrm:
        return await SourceOrm.get_or_create(libelle=source.libelle) # type: ignore
