up-airflow:
	docker compose -f docker-compose.airflow.yml up -d

up-scrap:
	docker compose -f docker-compose.scrap.yml -f docker-compose.db.yml up -d
	
up-db:
	docker compose -f docker-compose.db.yml up -d
	
down-all:
	docker compose \
	  -f docker-compose.airflow.yml \
	  -f docker-compose.scrap.yml \
	  -f docker-compose.db.yml \
	  down
