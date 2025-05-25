from app.celery_app import celery_client
import logging
import logging.config


# Configuration du logging
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/logs/worker.log',
            'formatter': 'standard'
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True
        },
        'app': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False
        },
        'celery': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False
        },
    }
})

# Créer un logger pour ce module
logger = logging.getLogger(__name__)
logger.info("Démarrage de l'application Celery")

celery_client.autodiscover_tasks([
    "app.workers.usecases.statique.test_scrap_detail",
    "app.workers.usecases.statique.test_scrap_summaries",
    "app.workers.usecases.statique.scrap_detail",
    "app.workers.usecases.statique.scrap_summaries",
])

logger.info("Tâches découvertes et enregistrées")
