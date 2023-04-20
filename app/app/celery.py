from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

app = Celery(
    "app",
    broker=settings.CELERY_BROKER_URL,
    include=["core.tasks"]
)
app.conf.enable_utc = True
app.conf.update(timezone="Europe/Kiev")


app.config_from_object(settings, namespace="CELERY")

# Celery Beat Settings
app.conf.beat_schedule = {
}

app.autodiscover_tasks()
