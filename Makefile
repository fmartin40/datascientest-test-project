airflow:
	docker compose -f docker-compose.airflow.yml up -d

scrap:
	docker compose -f docker-compose.scrap.yml -f docker-compose.db.yml up -d
	
db:
	docker compose -f docker-compose.db.yml up -d
	
down:
	docker compose \
	  -f docker-compose.airflow.yml \
	  -f docker-compose.scrap.yml \
	  -f docker-compose.db.yml \
	  down
