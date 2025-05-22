#!/bin/bash

# Nom du réseau
NETWORK_NAME="jobsearch_network"

# Vérifie si le réseau existe
if ! docker network ls --format '{{.Name}}' | grep -wq "$NETWORK_NAME"; then
  echo " Création du réseau Docker : $NETWORK_NAME"
  docker network create "$NETWORK_NAME"
else
  echo " Réseau Docker déjà existant : $NETWORK_NAME"
fi

# Liste des fichiers docker-compose à lancer
COMPOSE_FILES=(
  "docker-compose.postgres.yml"
  "docker-compose.scrap.yml"
  "docker-compose.celery.yml"
  "docker-compose.elastic.yml"
)

# Démarrage de chaque docker-compose
for FILE in "${COMPOSE_FILES[@]}"; do
  if [ -f "$FILE" ]; then
    echo " Lancement de $FILE"
    docker-compose -f "$FILE" up -d
  else
    echo " Fichier introuvable : $FILE"
  fi
done

