#!/bin/bash

# Nom du réseau
NETWORK_NAME="jobsearch_network"

# Vérifie si le réseau existe
if ! docker network ls --format '{{.Name}}' | grep -wq "$NETWORK_NAME"; then
  echo "Création du réseau Docker : $NETWORK_NAME"
  docker network create "$NETWORK_NAME"
else
  echo "Réseau Docker déjà existant : $NETWORK_NAME"
fi

# Liste des fichiers docker-compose à lancer (hors Airflow)
COMPOSE_FILES=(
  "docker-compose.postgres.yml"
  "docker-compose.elastic.yml"
  "docker-compose.celery.yml"
  "docker-compose.scrap.yml"
)

# Démarrage des services non-Airflow
for FILE in "${COMPOSE_FILES[@]}"; do
  if [ -f "$FILE" ]; then
    echo "Lancement de $FILE"

    if [[ "$FILE" == *"celery"* ]]; then
      echo "Scaling du service Celery à 4 workers"
      docker compose -f "$FILE" up -d --build
    else
      docker compose -f "$FILE" up -d --build
    fi
  else
    echo "Fichier introuvable : $FILE"
  fi
done

# Lancement de airflow-init
if [ -f "docker-compose.airflow.yml" ]; then
  echo "Initialisation d'Airflow"
  docker compose -f docker-compose.airflow.yml up airflow-init -d

  echo "Attente de la fin de l'initialisation d'Airflow..."

  # Attente jusqu'à ce que airflow-init s'arrête
  while true; do
    STATUS=$(docker inspect -f '{{.State.Status}}' airflow-init 2>/dev/null)
    EXIT_CODE=$(docker inspect -f '{{.State.ExitCode}}' airflow-init 2>/dev/null)

    if [ "$STATUS" == "exited" ]; then
      if [ "$EXIT_CODE" == "0" ]; then
        echo " Initialisation d'Airflow terminée avec succès."
        break
      else
        echo " Échec de l'initialisation d'Airflow (code de sortie $EXIT_CODE)."
        exit 1
      fi
    fi

    sleep 2
  done

  echo "Démarrage des services Airflow..."
  docker compose -f docker-compose.airflow.yml up -d --build
else
  echo "Fichier docker-compose.airflow.yml introuvable."
fi
