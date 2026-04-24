from celery import Celery
from app.core.config import settings


celery_app = Celery(
    "app",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=[
        "app.tasks.document_tasks",
        "app.tasks.embedding_tasks",
        "app.tasks.llm_tasks",
        ]
)

# celery_app.conf.task_routes = {
#     "app.tasks.*": {"queue": "default"},
# }

celery_app.autodiscover_tasks(["app.tasks"])
