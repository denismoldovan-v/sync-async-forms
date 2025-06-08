# celery_worker.py
from celery import Celery

celery = Celery(
    "whitefly",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

def init_celery(app):
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return super().__call__(*args, **kwargs)

    celery.Task = ContextTask

import async_tasks
