from celery import Celery
from app.server import celery_client
import app.workers.pipelines.scrap

