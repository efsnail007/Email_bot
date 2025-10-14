import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bot_backend.settings")
app = Celery("bot_backend")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "every": {
        "task": "email_server.tasks.send_request_bot",
        "schedule": crontab(),
    },
}
