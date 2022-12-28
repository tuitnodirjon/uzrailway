import os

from django.conf import settings

from celery import Celery

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "core.settings"
)

app = Celery("core")

app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks(settings.INSTALLED_APPS)
app.conf.beat_schedule = {
    "check_stations": {
        "task": "main.check_stations",
        "schedule": 30,  # 30 seconds
    },
}
