from app.infrastructure.dynamique.load.redis_loader import ILoader


async def get_competences(container=None)->list[str]:
    """
    Récupère la liste des compétences depuis Redis via le container.
    Si container n'est pas fourni, on retourne une liste par défaut.
    """
    if container is not None:
        try:
            # Supposons que tu as une méthode pour récupérer depuis Redis
            loader: ILoader = container.redis_loader()
            return await loader.get_competences()
        except Exception as e:
            print(f"Erreur lors de la récupération des compétences depuis Redis : {e}")
    return [
        "airflow",
        "amazon s3",
        "ansible",
        "apache beam",
        "apache spark",
        "argo workflows",
        "aws",
        "azure",
        "azure blob storage",
        "bigquery",
        "cassandra",
        "ci/cdcloud",
        "dagster",
        "datadog",
        "dask",
        "dbt",
        "docker",
        "dynamodb",
        "elasticsearch",
        "fivetran",
        "flink",
        "git",
        "github",
        "gitlab",
        "github actions",
        "gitlab ci/cd",
        "go",
        "google cloud storage",
        "grafana",
        "gcp",
        "hadoop hdfs",
        "helm",
        "informatica",
        "java",
        "jenkins",
        "kafka",
        "kinesis",
        "kubeflow",
        "kubernetes",
        "luigi",
        "matillion",
        "microsoft sql server",
        "mongodb",
        "mysql",
        "oracle db",
        "pandas",
        "postgresql",
        "prefect",
        "prometheus",
        "python",
        "redshift",
        "redis",
        "scala",
        "snowflake",
        "sql",
        "stitch",
        "talend",
        "terraform",
        "vault",
    ] 
    # Liste par défaut si pas de container ou erreur


async def get_mode_travail(container=None)->list[str]:
    """
    Récupère la liste des modes de travail depuis Redis via le container.
    Si container n'est pas fourni, on retourne une liste par défaut.
    """
    if container is not None:
        try:
            loader: ILoader = container.redis_loader()
            return await loader.get_mode_travail()
        except Exception as e:
            print(f"Erreur lors de la récupération des modes de travail depuis Redis : {e}")
    return [
        "Distanciel",
        "Hybride",
        "Présentiel",
    ]
    # Liste par défaut si pas de container ou erreur

async def get_type_contrat(container=None)->list[str]:
    """
    Récupère la liste des types de contrats depuis Redis via le container.
    Si container n'est pas fourni, on retourne une liste par défaut.
    """
    if container is not None:
        try:
            loader: ILoader = container.redis_loader()
            return await loader.get_type_contrat()
        except Exception as e:
            print(f"Erreur lors de la récupération des types de contrats depuis Redis : {e}")
    return [
        "CDI",
        "CDD",
        "Freelance",
        "Stage",
        "Alternance",
        "Temps partiel",
        "Temps plein",
    ]
    # Liste par défaut si pas de container ou erreur

async def get_source(container=None)->list[str]:
    """
    Récupère la liste des sources depuis Redis via le container.
    Si container n'est pas fourni, on retourne une liste par défaut.
    """
    if container is not None:
        try:
            loader: ILoader = container.redis_loader()
            return await loader.get_source()
        except Exception as e:
            print(f"Erreur lors de la récupération des sources depuis Redis : {e}")
    return [
        "LinkedIn", 
        "Indeed",
        "Glassdoor",
        "Monster",
        "Wanted",
        "Xing",
        "Xing",
    ]   