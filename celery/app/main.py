from app.celery_app import celery_client

celery_client.autodiscover_tasks(["app.workers.scrap","app.workers.test.summaries","app.workers.test.detail" ])
