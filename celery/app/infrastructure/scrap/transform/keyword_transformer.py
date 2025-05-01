from typing import Any, Dict
from app.workers.scrap.entities.jobs import JobDetail, JobDetailInfos
from app.workers.scrap.entities.settings import ParserSettings, WebsiteInfo
from app.workers.scrap.interfaces.itransformer import ITransformer
import re


class KeywordTransformer(ITransformer):
    def __init__(self, website_info: WebsiteInfo, parser: ParserSettings):
        self.website_info: WebsiteInfo = website_info
        self.parser: ParserSettings = parser
        self.technologies: set[str] = set()
        self.contract_types: set[str] = set()

    def _extract_keyword(self, job_description: str, keywords: set) -> set:
        normalized_text: str = re.sub(
            r"[^a-z0-9\s]", " ", job_description.lower()
        ).lower()
        found: set = set()
        for keyword in keywords:
            pattern: str = r"\b" + re.escape(keyword.lower()) + r"\b"
            if re.search(pattern, normalized_text):
                found.add(keyword)
        return found

    def _load_technologies(self) -> set[str]:
        self.technologies: set[str] = {
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
        }
        return self.technologies

    def _load_contract_types(self) -> set[str]:
        self.contract_types = {
            "CDI",
            "CDD",
            "Freelance",
            "Stage",
            "Permanent",
            "Part-time",
            "Temporary",
            "remote",
        }
        return self.contract_types

    async def transform(self, jobdetail: JobDetail) -> Dict[str, Any]:
        return {
            "technologies": self._extract_keyword(  # type: ignore
                jobdetail.description, set(self._load_technologies())
            ),
            "contract_types": self._extract_keyword(  # type: ignore
                jobdetail.description, set(self._load_contract_types())
            ),
        }  # type: ignore
