#!/bin/bash


# Liste des fichiers docker-compose à lancer
COMPOSE_FILES=(
  "docker-compose.airflow.yml"
  "docker-compose.scrap.yml"
  "docker-compose.celery.yml"
  "docker-compose.elastic.yml"
  "docker-compose.postgres.yml"
)

# Démarrage de chaque docker-compose
for FILE in "${COMPOSE_FILES[@]}"; do
  if [ -f "$FILE" ]; then
    echo " Arrêt de $FILE"
    docker compose -f "$FILE" down
  else
    echo " Fichier introuvable : $FILE"
  fi
done

echo " ATTENTION : Ce script va supprimer TOUS les volumes Docker."
read -p "Voulez-vous vraiment continuer ? (yes/no) " CONFIRM1

if [ "$CONFIRM1" == "yes" ]; then
  echo " Suppression de tous les volumes Docker..."
  docker volume rm $(docker volume ls -q)
  echo " Tous les volumes ont été supprimés."
else
  echo " Opération annulée."
fi

echo " ATTENTION : Ce script va supprimer TOUTES les images Docker."
read -p "Voulez-vous vraiment continuer ? (yes/no) " CONFIRM2

if [ "$CONFIRM2" == "yes" ]; then
  echo " Suppression de toutes les images Docker..."
  docker rmi $(docker images -q)
  echo " Toutes les images ont été supprimées."
else
  echo " Opération annulée."
fi

