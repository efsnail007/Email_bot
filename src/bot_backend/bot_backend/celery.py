import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bot_backend.settings")
app = Celery("bot_backend")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
