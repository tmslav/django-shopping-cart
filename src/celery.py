from __future__ import absolute_import
from datetime import timedelta

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')

from django.conf import settings

app = Celery('src')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.conf.update(
    CELERYBEAT_SCHEDULE = {
        'clean_memcached': {
            'task': 'tasks.clean_memcached',
            'schedule': timedelta(minutes=5),
        },
})

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

