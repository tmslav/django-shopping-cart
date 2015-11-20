from __future__ import absolute_import

import os

from celery import Celery
from celery.contrib import rdb

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')

from django.conf import settings

app = Celery('src')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(*args,**kwargs):
    rdb.set_trace()
    print args,kwargs