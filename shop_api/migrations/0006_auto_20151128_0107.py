# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('shop_api', '0005_auto_20151128_0053'),
    ]

    operations = [
        migrations.RenameField(
            model_name='memcachedkeys',
            old_name='last_user',
            new_name='last_used',
        ),
        migrations.RenameField(
            model_name='shoporders',
            old_name='key_memcached',
            new_name='key',
        ),
        migrations.AddField(
            model_name='shoporders',
            name='memcached_key',
            field=models.CharField(default=datetime.datetime(2015, 11, 28, 1, 7, 28, 610034, tzinfo=utc), max_length=200),
            preserve_default=False,
        ),
    ]
