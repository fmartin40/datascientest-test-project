#!/bin/bash

# Attendre qu'Elasticsearch soit prêt
until curl -s http://localhost:9200 > /dev/null; do
    echo "Waiting for Elasticsearch..."
    sleep 2
done

# Changer le mot de passe avec authentification
curl -X POST "localhost:9200/_security/user/kibana_system/_password" \
     -H "Content-Type: application/json" \
     -u "elastic:${ELASTIC_PASSWORD}" \
     -d "{\"password\":\"${KIBANA_SYSTEM_PASSWORD}\"}"