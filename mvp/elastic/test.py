from elasticsearch import Elasticsearch, helpers
import csv
import os
from pathlib import Path

# Connexion au cluster
es = Elasticsearch(hosts = "http://@localhost:9200")

def load_data():

    ROOT_DIR = Path(__file__).parent.parent
    CAR_FILE = os.path.join(ROOT_DIR, "docs", "EmployerReviews.csv")
    with open(CAR_FILE, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        helpers.bulk(es, reader, index='reviews')


if __name__ == "__main__":
    load_data()