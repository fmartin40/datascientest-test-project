from logging import getLogger
from datetime import date
from app.domain.job.interfaces.istat_reader import IStatsReader
from app.domain.job.entities.stats import CompetenceByDateStats
from app.infrastructure.models.models import CompetenceDateAgg, CompetenceOrm
from tortoise.functions import Sum
from collections import defaultdict

logger = getLogger(__name__)


class StatsReader(IStatsReader):
    async def list_competences_by_day(self, from_date: date, to_date: date):
        try:
            aggs = await CompetenceDateAgg.filter(
                date__gte=from_date, date__lte=to_date
            ).prefetch_related("competence")
            result = []
            for agg in aggs:
                result.append(
                    {
                        "competence": agg.competence.libelle,
                        "date": agg.date,
                        "count": agg.count,
                    }
                )
            # Regroupement par libellé
            grouped = defaultdict(list)
            for item in result:
                grouped[item["competence"]].append(
                    {"date": item["date"], "count": item["count"]}
                )
            return [
                {"competence": libelle, "values": values}
                for libelle, values in grouped.items()
            ]
        except Exception as e:
            logger.error(
                f"Erreur lors de la récupération des compétences par date : {e}"
            )
            raise

    async def sum_competences_by_date(
        self, from_date: date, to_date: date, competence_id: int | None = None
    ):
        try:
            if competence_id is not None:
                aggs = await CompetenceDateAgg.filter(
                    competence_id=competence_id, date__gte=from_date, date__lte=to_date
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
            else:
                aggs = (
                    await CompetenceDateAgg.filter(
                        date__gte=from_date, date__lte=to_date
                    )
                    .group_by("competence_id")
                    .annotate(total=Sum("count"))
                    .order_by("-total")
                    .prefetch_related("competence")
                )
                result = []
                for agg in aggs:
                    libelle = None
                    competence_id_val = getattr(agg, "competence_id", None)
                    total = getattr(agg, "total", None)
                    if hasattr(agg, "competence") and agg.competence:
                        libelle = agg.competence.libelle
                    else:
                        comp = await CompetenceOrm.get(id=competence_id_val)
                        libelle = comp.libelle
                    result.append(
                        {
                            "competence_id": competence_id_val,
                            "competence": libelle,
                            "total": total,
                        }
                    )
                return result
        except Exception as e:
            logger.error(f"Erreur lors de l'agrégation des compétences par date : {e}")
            raise
