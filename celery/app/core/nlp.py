import spacy

_NLP = None

def get_nlp():
    global _NLP
    if _NLP is None:
        _NLP = spacy.load("fr_core_news_sm")
    return _NLP

COMPETENCES =  [
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

MODE_TRAVAIL = [
            "teletravail",
            "presentiel",
            "hybride",
            "remote",
            "partial remote",
            "hybrid",
            "flexible",    
        ]

TYPE_CONTRAT = [
            "CDI",
            "CDD",
            "stage",
            "temporaire",
            "alternance",
        ]

DUREE_TRAVAIL = [
    "temps plein",
    "temps partiel",
    "temps complet",
    "full time",
    "part time",
]

