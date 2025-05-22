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

class SalaireOrm(Model):
    id = fields.IntField(pk=True)
    libelle = fields.TextField(null=True)

    class Meta:
        table = "Salaire"

class FormationOrm(Model):
    id = fields.IntField(pk=True)
    libelle = fields.TextField(null=True, source_field="libelle")

    class Meta:
        table = "Formation"

class LangueOrm(Model):
    id = fields.IntField(pk=True)
    libelle = fields.CharField(max_length=255, unique=True, source_field="libelle")

    class Meta:
        table = "Langue"

class ExperienceOrm(Model):
    id = fields.IntField(pk=True)
    libelle = fields.CharField(max_length=255, null=True, source_field="libelle")

    class Meta:
        table = "Experience"

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
    type_contrat = fields.CharField(max_length=255, null=True, source_field="typeContrat")

    experience = fields.ForeignKeyField(
        "models.ExperienceOrm", related_name="offres", null=True, source_field="experience_id"
    )
    duree_travail = fields.ForeignKeyField(
        "models.DureeTravailOrm", related_name="offres", null=True, source_field="duree_travail_id"
    )
    entreprise = fields.ForeignKeyField(
        "models.EntrepriseOrm", related_name="offres", null=True, source_field="entreprise_id"
    )
    ville = fields.ForeignKeyField(
        "models.VilleOrm", related_name="offres", null=True, source_field="ville_id"
    )
    salaire = fields.ForeignKeyField(
        "models.SalaireOrm", related_name="offres", null=True, source_field="salaire_id"
    )
    mode_travail = fields.ForeignKeyField(
        "models.ModeTravailOrm", related_name="offres", null=True, source_field="mode_travail_id"
    )
    type_contrat = fields.ForeignKeyField(
        "models.TypeContratOrm", related_name="offres", null=True, source_field="type_contrat_id"
    )
    source = fields.ForeignKeyField(
        "models.SourceOrm", related_name="offres", null=True, source_field="source_id"
    )

    formations = fields.ManyToManyField(
        "models.FormationOrm", related_name="offres", through="OffreEmploi_Formation",
        forward_key="formation_id", backward_key="offre_id"
    )
    langues = fields.ManyToManyField(
        "models.LangueOrm", related_name="offres", through="OffreEmploi_Langue",
        forward_key="langue_id", backward_key="offre_id"
    )
    competences = fields.ManyToManyField(
        "models.CompetenceOrm", related_name="offres", through="OffreEmploi_Competence",
        forward_key="competence_id", backward_key="offre_id"
    )

    class Meta:
        table = "OffreEmploi"

class OffreEmploiFormationOrm(Model):
    offre_id = fields.ForeignKeyField(
        "models.OffreEmploiOrm", related_name="offre_formation", source_field="offre_id"
    )
    formation = fields.ForeignKeyField(
        "models.FormationOrm", related_name="formation_offre", source_field="formation_id"
    )

    class Meta:
        table = "OffreEmploi_Formation"
        unique_together = (("offre", "formation"),)

class OffreEmploiLangueOrm(Model):
    offre_id = fields.ForeignKeyField(
        "models.OffreEmploiOrm", related_name="offre_langue", source_field="offre_id"
    )
    langue = fields.ForeignKeyField(
        "models.LangueOrm", related_name="langue_offre", source_field="langue_id"
    )

    class Meta:
        table = "OffreEmploi_Langue"
        unique_together = (("offre", "langue"),)

class OffreEmploiCompetenceOrm(Model):
    offre_id = fields.ForeignKeyField(
        "models.OffreEmploiOrm", related_name="offre_competence", source_field="offre_id"
    )
    competence = fields.ForeignKeyField(
        "models.CompetenceOrm", related_name="competence_offre", source_field="competence_id"
    )

    class Meta:
        table = "OffreEmploi_Competence"
        unique_together = (("offre", "competence"),)
