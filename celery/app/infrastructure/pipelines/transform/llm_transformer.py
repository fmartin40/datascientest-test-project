import re
from sentence_transformers import SentenceTransformer
from app.workers.common.entities.jobs import JobDetail, JobDetailInfos
from app.workers.common.entities.settings import ParserSettings, WebsiteInfo
from app.workers.common.interfaces.itransformer import ITransformer

tech_keywords: set[str] = {
    "python",
    "sql",
    "java",
    "scala",
    "go",
    "postgresql",
    "mysql",
    "oracle db",
    "microsoft sql server",
    "mongodb",
    "cassandra",
    "redis",
    "elasticsearch",
    "dynamodb",
    "snowflake",
    "bigquery",
    "redshift",
    "apache airflow",
    "dbt",
    "talend",
    "informatica",
    "fivetran",
    "stitch",
    "matillion",
    "apache kafka",
    "apache flink",
    "apache pulsar",
    "amazon kinesis",
    "amazon s3",
    "google cloud storage",
    "azure blob storage",
    "hadoop hdfs",
    "apache spark",
    "dask",
    "pandas",
    "apache beam",
    "prefect",
    "dagster",
    "luigi",
    "kubeflow",
    "argo workflows",
    "terraform",
    "ansible",
    "cloudformation",
    "docker",
    "kubernetes",
    "helm",
    "aws",
    "gcp",
    "azure",
    "prometheus",
    "grafana",
    "elk stack",
    "datadog",
    "git",
    "github actions",
    "gitlab ci/cd",
    "jenkins",
    "vault",
    "aws iam",
    "gcp iam",
}


class LLMTransformer(ITransformer):
    def __init__(self, website_info: WebsiteInfo, parser: ParserSettings):
        self.website_info: WebsiteInfo = website_info
        self.parser: ParserSettings = parser
        # self.jobdetail: JobDetail = None

    def _extract_keyword(self, job_description: str, tech_keywords: set) -> set:
        normalized_text: str = re.sub(r"[^a-z0-9\s]", " ", job_description.lower()).lower()
        found: set = set()
        for keyword in tech_keywords:
            pattern: str = r"\b" + re.escape(keyword.lower()) + r"\b"
            if re.search(pattern, normalized_text):
                found.add(keyword)
        return found
    
    def _embeddings(self, job_description: str) -> list[float]:
        model = SentenceTransformer('quora-distilbert-multilingual')
        result = model.encode(job_description, show_progress_bar=False).tolist()
        return result

    async def transform(self, jobdetail: JobDetail) -> JobDetail:
        jobdetail.infos = JobDetailInfos(
            technologies=list(self._extract_keyword(jobdetail.description, tech_keywords)),
            embeddings=self._embeddings(jobdetail.description)
        )

        return jobdetail
