from tortoise import fields
from tortoise.models import Model


class EntrepriseOrm(Model):
    id = fields.IntField(pk=True)
    libelle = fields.CharField(max_length=255, null=True)

    class Meta:
        table = "Entreprise"


class VilleOrm(Model):
    id = fields.IntField(pk=True)
    libelle = fields.CharField(max_length=255, null=True)

    class Meta:
        table = "Ville"


class DureeTravailOrm(Model):
    id = fields.IntField(pk=True)
    libelle = fields.CharField(max_length=255, null=True, source_field="libelle")

    class Meta:
        table = "DureeTravail"


class CompetenceOrm(Model):
    id = fields.IntField(pk=True)
    libelle = fields.CharField(max_length=255, null=True, source_field="libelle")

    class Meta:
        table = "Competence"


class ModeTravailOrm(Model):
    id = fields.IntField(pk=True)
    libelle = fields.CharField(max_length=50, unique=True, null=False)

    class Meta:
        table = "ModeTravail"


class TypeContratOrm(Model):
    id = fields.IntField(pk=True)
    libelle = fields.CharField(max_length=50, unique=True, null=False)

    class Meta:
        table = "TypeContrat"


class SourceOrm(Model):
    id = fields.IntField(pk=True)
    libelle = fields.CharField(max_length=255, null=True, source_field="libelle")

    class Meta:
        table = "Source"


class OffreEmploiOrm(Model):
    id = fields.IntField(pk=True)
    job_id = fields.CharField(max_length=255, null=True, source_field="jobId")
    date_creation = fields.DateField(null=True, source_field="dateCreation")
    libelle = fields.CharField(max_length=255, null=True, source_field="libelle")
    url = fields.CharField(max_length=255, null=True, source_field="url")
    # type_contrat = fields.CharField(
    #     max_length=255, null=True, source_field="typeContrat"
    # )

    duree_travail = fields.ForeignKeyField(
        "models.DureeTravailOrm",
        related_name="offres",
        null=True,
        source_field="duree_travail_id",
    )
    entreprise = fields.ForeignKeyField(
        "models.EntrepriseOrm",
        related_name="offres",
        null=True,
        source_field="entreprise_id",
    )
    ville = fields.ForeignKeyField(
        "models.VilleOrm", related_name="offres", null=True, source_field="ville_id"
    )
    mode_travail = fields.ForeignKeyField(
        "models.ModeTravailOrm",
        related_name="offres",
        null=True,
        source_field="mode_travail_id",
    )
    type_contrat = fields.ForeignKeyField(
        "models.TypeContratOrm",
        related_name="offres",
        null=True,
        source_field="type_contrat_id",
    )
    source = fields.ForeignKeyField(
        "models.SourceOrm", related_name="offres", null=True, source_field="source_id"
    )

    competences = fields.ManyToManyField(
        "models.CompetenceOrm",
        related_name="offres",
        through="OffreEmploi_Competence",
        forward_key="competence_id",
        backward_key="offre_id",
    )

    class Meta:
        table = "OffreEmploi"


class OffreEmploiCompetenceOrm(Model):
    offre_id = fields.ForeignKeyField(
        "models.OffreEmploiOrm",
        related_name="offre_competence",
        source_field="offre_id",
    )
    competence = fields.ForeignKeyField(
        "models.CompetenceOrm",
        related_name="competence_offre",
        source_field="competence_id",
    )

    class Meta:
        table = "OffreEmploi_Competence"
        unique_together = (("offre", "competence"),)


# --- Mappings entre libellés et entités ---


class MappingTypeContratOrm(Model):
    id = fields.IntField(pk=True)
    libelle = fields.CharField(max_length=100, unique=True, null=False)
    type_contrat = fields.ForeignKeyField(
        "models.TypeContratOrm",
        related_name="mappings_type_contrat",
        null=True,
        source_field="type_contrat_id",
        on_delete=fields.CASCADE,
    )

    class Meta:
        table = "MappingTypeContrat"


class MappingModeTravailOrm(Model):
    id = fields.IntField(pk=True)
    libelle = fields.CharField(max_length=100, unique=True, null=False)
    mode_travail = fields.ForeignKeyField(
        "models.ModeTravailOrm",
        related_name="mappings_mode_travail",
        null=True,
        source_field="mode_travail_id",
        on_delete=fields.CASCADE,
    )

    class Meta:
        table = "MappingModeTravail"


class MappingDureeTravailOrm(Model):
    id = fields.IntField(pk=True)
    libelle = fields.CharField(max_length=100, unique=True, null=False)
    duree_travail = fields.ForeignKeyField(
        "models.DureeTravailOrm",
        related_name="mappings_duree_travail",
        null=True,
        source_field="duree_travail_id",
        on_delete=fields.CASCADE,
    )

    class Meta:
        table = "MappingDureeTravail"


class MappingCompetenceOrm(Model):
    id = fields.IntField(pk=True)
    libelle = fields.CharField(max_length=100, unique=True, null=False)
    competence = fields.ForeignKeyField(
        "models.CompetenceOrm",
        related_name="mappings_competence",
        null=True,
        source_field="competence_id",
        on_delete=fields.CASCADE,
    )

    class Meta:
        table = "MappingCompetence"


class CompetenceDateAgg(Model):
    id = fields.IntField(pk=True)
    competence = fields.ForeignKeyField(
        "models.CompetenceOrm", related_name="date_aggs"
    )
    date = fields.DateField()
    count = fields.IntField(default=0)

    class Meta:
        table = "CompetenceDateAgg"
        unique_together = (("competence", "date"),)
        indexes = [("competence", "date")]


class CompetenceDateBuffer(Model):
    id = fields.IntField(pk=True)
    competence = fields.ForeignKeyField(
        "models.CompetenceOrm", related_name="date_buffers"
    )
    date = fields.DateField()

    class Meta:
        table = "CompetenceDateBuffer"
        unique_together = (("competence", "date"),)
