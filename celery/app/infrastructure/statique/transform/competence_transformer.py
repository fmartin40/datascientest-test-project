from typing import Any, List
from app.workers.scrap.interfaces.itransformer import ITransformer
import re


class CompetencesTransformer(ITransformer):
    def __init__(self):
        self.competences: list[str] = []
        self._load_competences()   
        
    def _extract_keyword(self, text: str) -> list[str]:
        normalized_text: str = re.sub(
            r"[^a-z0-9\s]", " ", text.lower()
        ).lower()
        found: set = set()
        for keyword in self.competences:
            pattern: str = r"\b" + re.escape(keyword.lower()) + r"\b"
            if re.search(pattern, normalized_text):
                found.add(keyword)
        return list(found)
    
    def _extract_llm(self, text: str) -> set:
        raise NotImplementedError("LLM extraction not implemented")

    def _load_competences(self) -> None:
        self.competences: list[str] = [
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
        # return self.competence


    async def transform(self, text:str, llm:bool=False) -> List[str]:
        if llm:
            return []
        else:
            return self._extract_keyword(text)
