from app.workers.scrap.interfaces.itransformer import ITransformer
from app.workers.scrap.entities.jobs import JobDetail
import spacy
from spacy.matcher import PhraseMatcher

import logging
from app.core.nlp import get_nlp

logger = logging.getLogger(__name__)

class CompetencesTransformer(ITransformer):
    def __init__(self, container=None):
        self.container = container
        

    async def transform(self, job_detail:JobDetail, llm:bool=False) -> JobDetail:
        
        if llm:
            job_detail.competence = self._extract_keyword(job_detail.description)
        else:
            job_detail.competence = self._extract_keyword(job_detail.description)
        return job_detail
      
    def _extract_keyword(self, text: str) -> list[str]:
        nlp = get_nlp()
        doc = nlp(text)
        competences: list[str] = self._load_competences()
        # Préparation du PhraseMatcher
        matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
        patterns = [nlp.make_doc(text) for text in competences]
        matcher.add("CIBLES", patterns)

        # Recherche des matches
        matches = matcher(doc)
        found_keywords = [doc[start:end].text for match_id, start, end in matches]

        # Afficher les extraits trouvés
        logger.info(f"Expressions trouvées : {found_keywords}")
        return found_keywords
    
    def _extract_llm(self, text: str) -> set:
        raise NotImplementedError("LLM extraction not implemented")

    def _load_competences(self) -> list[str]:
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
        # return self.competence


