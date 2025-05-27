from logging import getLogger
from datetime import date
from app.domain.job.interfaces.istat_reader import IStatsReader
from app.domain.job.entities.stats import CompetenceByDateStats
from app.infrastructure.models.models import CompetenceDateAgg, CompetenceOrm
from tortoise.functions import Sum

logger = getLogger(__name__)


class StatsReader(IStatsReader):
    async def list_competences_by_date(self, date_debut: date, date_fin: date):
        try:
            aggs = await CompetenceDateAgg.filter(
                date__gte=date_debut, date__lte=date_fin
            ).prefetch_related("competence")
            result = []
            for agg in aggs:
                result.append(
                    CompetenceByDateStats(
                        date=agg.date,
                        competence_id=agg.competence.id,
                        competence_libelle=agg.competence.libelle,
                        count=agg.count,
                    )
                )
            return result
        except Exception as e:
            logger.error(
                f"Erreur lors de la récupération des compétences par date : {e}"
            )
            return []

    async def get_competence_by_date(
        self, competence_id: int, date_debut: date, date_fin: date
    ):
        try:
            aggs = await CompetenceDateAgg.filter(
                competence_id=competence_id, date__gte=date_debut, date__lte=date_fin
            ).prefetch_related("competence")
            result = []
            for agg in aggs:
                result.append(
                    CompetenceByDateStats(
                        date=agg.date,
                        competence_id=agg.competence.id,
                        competence_libelle=agg.competence.libelle,
                        count=agg.count,
                    )
                )
            return result
        except Exception as e:
            logger.error(
                f"Erreur lors de la récupération de la compétence {competence_id} par date : {e}"
            )
            return []

    async def sum_competences_by_date(self, date_debut: date, date_fin: date):
        try:
            aggs = (
                await CompetenceDateAgg.filter(date__gte=date_debut, date__lte=date_fin)
                .group_by("competence_id")
                .annotate(total=Sum("count"))
                .order_by("-total")
                .prefetch_related("competence")
            )
            result = []
            for agg in aggs:
                # On récupère le libellé de la compétence
                libelle = None
                competence_id = getattr(agg, "competence_id", None)
                total = getattr(agg, "total", None)
                if hasattr(agg, "competence") and agg.competence:
                    libelle = agg.competence.libelle
                else:
                    # fallback si prefetch ne marche pas
                    comp = await CompetenceOrm.get(id=competence_id)
                    libelle = comp.libelle
                result.append(
                    {
                        "competence_id": competence_id,
                        "competence_libelle": libelle,
                        "total": total,
                    }
                )
            return result
        except Exception as e:
            logger.error(f"Erreur lors de l'agrégation des compétences par date : {e}")
            return []
