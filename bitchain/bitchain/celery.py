# bitchain/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bitchain.settings')

app = Celery('bitchain')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.timezone = 'Europe/Warsaw'

app.conf.beat_schedule = {
    'reset_crypto_review_counts': {
        'task': 'crypto_reviews.tasks.reset_counts',
        'schedule': crontab(hour=0, minute=0),  # Execute daily at midnight
        'args': (),
    },
}


app.autodiscover_tasks()
