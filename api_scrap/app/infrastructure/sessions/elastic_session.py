from elasticsearch import Elasticsearch
from app.core.config import settings


def get_elastic_session()->Elasticsearch:
    return Elasticsearch(hosts=[settings.ELASTIC_HOST])