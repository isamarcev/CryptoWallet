from celery import Celery

from base_api.config.settings import settings

celery_app = Celery(
    "worker",
    backend="rpc://",
    # backend=settings.redis_url,
    broker="amqp://guest:guest@localhost:5672//"
    # broker=settings.redis_url
)

celery_app.conf.update(task_track_started=True)
celery_app.autodiscover_tasks(["base_api.apps.ethereum.tasks"])