airflow:
	docker compose -f docker-compose.airflow.yml up -d

scrap:
	docker compose -f docker-compose.scrap.yml up -d

celerylery:
	docker compose -f docker-compose.celery.yml up -d

postgres:
	docker compose -f docker-compose.postgres.yml up -d

elastic:
	docker compose -f docker-compose.elastic.yml up -d

down:
	docker compose \
	  -f docker-compose.airflow.yml \
	  -f docker-compose.scrap.yml \
	  -f docker-compose.celery.yml \
	  -f docker-compose.postgres.yml \
	  -f docker-compose.elastic.yml \
	  down
