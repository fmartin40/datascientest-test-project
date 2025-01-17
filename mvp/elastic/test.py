from elasticsearch import Elasticsearch, helpers
import csv
import os
from pathlib import Path

# Connexion au cluster
es = Elasticsearch(hosts = "http://@localhost:9200")

# Décommenter cette commande si vous utilisez l'installation sécurisée avec 3 nodes

#es = Elasticsearch(hosts = "https://elastic:datascientest@localhost:9200",
#                  ca_certs="./ca/ca.crt")

def load_data():

    ROOT_DIR = Path(__file__).parent.parent
    CAR_FILE = os.path.join(ROOT_DIR, "docs", "cars.csv")
    with open(CAR_FILE, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        helpers.bulk(es, reader, index='cars')


if __name__ == "__main__":
    load_data()