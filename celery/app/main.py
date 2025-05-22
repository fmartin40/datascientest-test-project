from app.celery_app import celery_client

celery_client.autodiscover_tasks([
    "app.workers.scrap.usecases.test_scrap_detail",
    "app.workers.scrap.usecases.test_scrap_summaries",
    "app.workers.scrap.usecases.scrap_detail",
    "app.workers.scrap.usecases.scrap_summaries",
])
